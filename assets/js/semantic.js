/**
 * Tier 2 search: re-rank BM25 hits by embedding similarity.
 *
 * MODEL_ID must match tools/embed.mjs exactly. Document vectors were computed
 * there with the same library; a mismatch yields meaningless scores with no
 * visible error, so this constant is not to be changed on one side alone.
 */
const MODEL_ID = 'Xenova/all-MiniLM-L6-v2';
const LIBRARY = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1/+esm';

let ready = null;

function cosine(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i += 1) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}

async function load() {
  const [{ pipeline }, response] = await Promise.all([
    import(/* webpackIgnore: true */ LIBRARY),
    fetch('assets/data/embeddings.json'),
  ]);
  const store = await response.json();

  if (store.model !== MODEL_ID) {
    throw new Error(
      `embeddings.json was built with ${store.model} but this page expects ${MODEL_ID}`,
    );
  }

  const extractor = await pipeline('feature-extraction', MODEL_ID);
  return { extractor, vectors: store.vectors };
}

window.__loadSemantic = () => {
  if (ready) return;
  ready = load().then(({ extractor, vectors }) => {
    window.__searchRerank = async (query, hits, docs) => {
      const output = await extractor(query, { pooling: 'mean', normalize: true });
      const queryVector = Array.from(output.data);

      // Score every document, not only the BM25 hits: the whole point is to
      // surface papers that share no vocabulary with the query.
      const scored = Object.entries(vectors)
        .map(([id, vector]) => ({ id, score: cosine(queryVector, vector) }))
        .filter((hit) => docs.has(hit.id) && hit.score > 0.15)
        .sort((a, b) => b.score - a.score)
        .slice(0, 8);

      return scored.length ? scored : hits;
    };
  }).catch(() => {
    // Tier 1 stands. Deliberately silent: the visitor has working search.
    ready = null;
  });
};
