/**
 * BM25 ranking over a small in-memory corpus.
 * Pure logic, no DOM: this file is unit-tested under Node.
 */

const STOPWORDS = new Set([
  'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can',
  'her', 'was', 'one', 'our', 'out', 'his', 'has', 'had', 'were', 'they',
  'this', 'that', 'with', 'from', 'their', 'which', 'when', 'what', 'have',
  'been', 'more', 'than', 'them', 'these', 'those', 'into', 'also', 'such',
  'does', 'how', 'why', 'who', 'its', 'it', 'as', 'at', 'by', 'in', 'of',
  'on', 'or', 'to', 'is', 'be', 'we', 'an', 'a',
]);

export function tokenize(text) {
  return String(text)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .split(/[^a-z0-9]+/)
    .filter((token) => token.length > 1 && !STOPWORDS.has(token));
}

export function buildIndex(docs) {
  const df = new Map();
  const entries = docs.map((doc) => {
    const tokens = tokenize(doc.text);
    const tf = new Map();
    tokens.forEach((token) => tf.set(token, (tf.get(token) || 0) + 1));
    tf.forEach((_, token) => df.set(token, (df.get(token) || 0) + 1));
    return { id: doc.id, tf, length: tokens.length };
  });

  const total = entries.reduce((sum, entry) => sum + entry.length, 0);
  return {
    entries,
    df,
    N: entries.length,
    avgdl: entries.length ? total / entries.length : 0,
  };
}

export function search(index, query, options = {}) {
  const { k1 = 1.5, b = 0.75, limit = 10 } = options;
  const terms = tokenize(query);
  if (terms.length === 0) return [];

  const results = [];
  index.entries.forEach((entry) => {
    let score = 0;
    terms.forEach((term) => {
      const freq = entry.tf.get(term);
      if (!freq) return;
      const n = index.df.get(term) || 0;
      const idf = Math.log(1 + (index.N - n + 0.5) / (n + 0.5));
      const norm = 1 - b + (b * entry.length) / (index.avgdl || 1);
      score += idf * ((freq * (k1 + 1)) / (freq + k1 * norm));
    });
    if (score > 0) results.push({ id: entry.id, score });
  });

  return results.sort((a, b2) => b2.score - a.score).slice(0, limit);
}
