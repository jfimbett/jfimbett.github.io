# llm_etr_pipeline.py
# -----------------------------------------------------------
# Purpose :  end-to-end demo – extract Income-Tax footnotes from
#            Apple 10-Ks and predict Δ-ETR with an LLM
# SDK     :  openai-python ≥ 1.76.x  (April-2025)
# Author  :  <you>
# Date    :  2025-05-02
# -----------------------------------------------------------
#%%
import json
import os
import re
import time
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import requests
from openai import OpenAI

###############################################################################
# 0.  CONFIGURATION  –––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
###############################################################################

client = OpenAI()                    # reads your OPENAI_API_KEY env-var
OPENAI_MODEL = "o4-mini"

TEMPERATURE_EXTRACT = 1.0            # deterministic grab
TEMPERATURE_PREDICT = 0.2            # mild variety for predictions

# ----------  SEC EDGAR  ------------------------------------------------------
CIK = "0000320193"                   # Apple Inc.
SUBMISSIONS_JSON = f"https://data.sec.gov/submissions/CIK{CIK}.json"
# ------------------------------------------------------------------
# SEC request headers – tuned to match a normal desktop browser
# ------------------------------------------------------------------
SEC_HEADERS = {
    # Identify your script (required by the SEC — use a real email)
    "User-Agent": "LLM-ETR-Research/1.0 (your.name@university.edu)",

    # Same Accept / language preferences the browser sent
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",

    # Brotli (`br`) is fine; zstd isn’t negotiated by requests yet, so omit it
    "Accept-Encoding": "gzip, deflate, br",

    # Standard connection hints
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",

    # “Fetch” hints (harmless for GET requests)
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",

    # Optional: a fixed If-Modified-Since value; safe to leave in
    "If-Modified-Since": "Thu, 19 Oct 2017 14:59:27 GMT",

    # ⚠️  COOKIE NOTE:
    # The ak_bmsc / bm_* cookies are anti-bot tokens that expire quickly.
    # Including stale values can *cause* 403s.  Uncomment the next line only
    # if you constantly refresh them yourself.
    # "Cookie": "ak_bmsc=…; bm_mi=…; bm_sv=…",
}

#
DOWNLOAD_PAUSE = 0.25                # polite delay between requests

# ----------  LOCAL CACHE  ----------------------------------------------------
CACHE_DIR = Path("cache_10k_html")
CACHE_DIR.mkdir(exist_ok=True)

###############################################################################
# 1.  EDGAR HELPERS  –––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
###############################################################################

def _safe_get(url: str) -> requests.Response:
    resp = requests.get(url, headers=SEC_HEADERS)
    time.sleep(DOWNLOAD_PAUSE)
    return resp


def _get_submissions() -> Dict:
    p = CACHE_DIR / "submissions.json"
    if p.exists():
        return json.loads(p.read_text())
    r = _safe_get(SUBMISSIONS_JSON)
    r.raise_for_status()
    p.write_text(r.text)
    return r.json()


def get_10k_index() -> pd.DataFrame:
    subs = _get_submissions()
    recent = pd.DataFrame(subs["filings"]["recent"])
    mask = recent["form"].str.contains(r"10-K", na=False)
    df = recent.loc[mask, ["accessionNumber", "primaryDocument", "filingDate"]]
    df["year"] = pd.to_datetime(df["filingDate"]).dt.year
    return df.sort_values("year").reset_index(drop=True)


# ----------  directory-listing helpers  --------------------------------------

ACC_TXT_RE = re.compile(r"^\d{10,}-\d{2}-\d+\.txt$", re.I)

def _extract_filenames(html: str) -> List[str]:
    """Return every *.htm/html/txt name shown in a folder listing page."""
    patt_anchor = r'href="([^"?/]+\.(?:htm|html|txt))"'
    patt_plain  = r'([^<>/]+\.(?:htm|html|txt))'
    files = set(re.findall(patt_anchor, html, flags=re.I))
    files.update(re.findall(patt_plain,  html, flags=re.I))
    return list(files)


def _score_candidate(name: str) -> tuple[int, int]:
    """
    Pick the best 10-K file available.  Lower tuple wins.

        (0,0)  accession-number.txt  – contains *entire* submission
        (1,0)  *10k*.htm|html        – explicit 10-K HTML
        (1,1)  *10k*.txt             – 10-K plain text
        (2,0)  other .txt            – fallback, but still whole filing
        (3,0)  any .htm|html         – last resort
    """
    lower = name.lower()

    if lower.endswith(".txt"):
        if ACC_TXT_RE.match(lower):
            return (0, 0)
        if "10k" in lower or "10-k" in lower:
            return (1, 1)
        return (2, 0)

    # html / htm
    if "10k" in lower or "10-k" in lower:
        return (1, 0)
    return (3, 0)


def _choose_filing_file(no_dashes: str) -> str:
    """
    Pick the preferred file in an accession folder.
    1️⃣  Try {base}/index.json
    2️⃣  Scrape HTML directory listing otherwise.
    """
    base = f"https://www.sec.gov/Archives/edgar/data/{int(CIK):d}/{no_dashes}"

    # JSON index first
    r = _safe_get(f"{base}/index.json")
    if r.ok and r.headers.get("Content-Type", "").startswith("application/json"):
        try:
            j = r.json()
            files = [f["name"] for f in j["directory"]["item"]]
            if files:
                return min(files, key=_score_candidate)
        except json.JSONDecodeError:
            pass

    # HTML listing fallback
    html = _safe_get(f"{base}/").text
    files = _extract_filenames(html)
    if not files:
        raise FileNotFoundError(f"No candidate 10-K file in {base}/")
    return min(files, key=_score_candidate)


def _download_filing_html(acc_no: str, primary_doc: str) -> str:
    """
    Download filing HTML (cache to disk).  If primaryDocument is 404
    fall back to directory discovery rules above.
    """
    no_dashes = acc_no.replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{int(CIK):d}/{no_dashes}"
    cache_file = CACHE_DIR / f"{no_dashes}.html"

    if cache_file.exists():
        return cache_file.read_text(errors="ignore")

    # attempt ① – primaryDocument
    url = f"{base}/{primary_doc.strip()}"
    resp = _safe_get(url)

    # attempt ② – best candidate in folder
    if resp.status_code == 404:
        best = _choose_filing_file(no_dashes)
        url  = f"{base}/{best}"
        resp = _safe_get(url)

    resp.raise_for_status()
    cache_file.write_text(resp.text, encoding="utf-8", errors="ignore")
    return resp.text


###############################################################################
# 2.  LLM UTILITIES – extract & predict  –––––––––––––––––––––––––––––––––––– #
###############################################################################

def extract_tax_footnote_llm(filing_html: str) -> str:
    system = (
        "You are an expert SEC analyst. From the 10-K below, copy-paste (verbatim) "
        "the single footnote that discusses income taxes. Return ONLY that text."
    )
    user = "<FILING_HTML>\n" + filing_html + "\n</FILING_HTML>"

    res = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE_EXTRACT,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    content = res.choices[0].message.content
    if not content:
        raise ValueError("LLM extraction returned empty content.")
    return content.strip()


def predict_etr_delta_llm(foot_tm1: str, foot_t: str) -> Dict:
    prompt = f"""
I will present you with two tax footnotes extracted from 10-K filings of the
same company, for consecutive fiscal years t-1 and t.

Based **only** on this information, decide whether the effective tax rate (ETR)
will **increase** or **decrease** from t-1 to t.

Return a JSON object with:
  "prediction":  +1 if ETR will RISE, -1 if ETR will FALL
  "explanation": ONE short sentence explaining why.

Footnote at time t:
{foot_t}

Footnote at time t-1:
{foot_tm1}
""".strip()

    res = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=TEMPERATURE_PREDICT,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    raw = res.choices[0].message.content or ""
    obj = json.loads(raw)
    if obj.get("prediction") not in (1, -1):
        raise ValueError(f"Bad prediction JSON:\n{raw}")
    return obj


###############################################################################
# 3.  PIPELINE  ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
###############################################################################

def run_pipeline() -> pd.DataFrame:
    print("Fetching 10-K index …")
    filings = get_10k_index()

    footnotes: Dict[int, str] = {}
    for _, row in filings.iterrows():
        yr = int(row["year"])
        print(f"  • {yr} – downloading & extracting footnote …")
        html = _download_filing_html(row["accessionNumber"], row["primaryDocument"])
        footnotes[yr] = extract_tax_footnote_llm(html)

    preds: List[Dict] = []
    years = sorted(footnotes)
    for i in range(1, len(years)):
        y_tm1, y_t = years[i-1], years[i]
        print(f"Predicting Δ-ETR {y_tm1} → {y_t} …")
        res = predict_etr_delta_llm(footnotes[y_tm1], footnotes[y_t])
        res["year"] = y_t
        preds.append(res)

    return pd.DataFrame(preds).set_index("year")


###############################################################################
# 4.  MANUAL ETR SERIES  ––––––––––––––––––––––––––––––––––––––––––––––––––– #
###############################################################################

ETR_SERIES = pd.DataFrame(
    dict(
        year=[2015, 2016, 2017, 2018, 2019,
              2020, 2021, 2022, 2023, 2024],
        etr =[26.4, 25.6, 24.6, 18.3, 15.9,
              14.4, 13.3, 16.2, 14.7, 24.1],
    )
).astype({"year": int, "etr": float}).set_index("year")
ETR_SERIES["delta_etr"] = ETR_SERIES["etr"].diff()

###############################################################################
# 5.  MAIN  –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
###############################################################################

#%%
if __name__ == "__main__":
    predictions = run_pipeline()

    combined = ETR_SERIES.join(predictions, how="left")
    combined.to_csv("apple_etr_predictions.csv")
    print("\nSaved ➜ apple_etr_predictions.csv\n")
    print(combined)

    ax = ETR_SERIES["delta_etr"].plot(
        title="Apple – Δ Effective Tax Rate (realised)",
        xlabel="Fiscal Year",
        ylabel="Δ ETR (percentage-points)",
        marker="o",
        grid=True,
    )
    plt.tight_layout()
    plt.show()
