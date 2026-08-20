/**
 * Two-component PCA by power iteration with deflation.
 * Deterministic by construction: the initial vector is a fixed function of
 * the index, never random, because the output is committed to the repository.
 */

function normalise(vector) {
  let norm = 0;
  for (let i = 0; i < vector.length; i += 1) norm += vector[i] * vector[i];
  norm = Math.sqrt(norm) || 1;
  for (let i = 0; i < vector.length; i += 1) vector[i] /= norm;
  return vector;
}

function dot(a, b) {
  let total = 0;
  for (let i = 0; i < a.length; i += 1) total += a[i] * b[i];
  return total;
}

export function pca2(vectors, iterations = 300) {
  const n = vectors.length;
  if (n === 0) return [];
  const d = vectors[0].length;

  const mean = new Float64Array(d);
  vectors.forEach((vector) => {
    for (let i = 0; i < d; i += 1) mean[i] += vector[i];
  });
  for (let i = 0; i < d; i += 1) mean[i] /= n;

  const centred = vectors.map((vector) =>
    Float64Array.from({ length: d }, (_, i) => vector[i] - mean[i]));

  let residual = centred.map((row) => Float64Array.from(row));
  const components = [];

  for (let c = 0; c < 2; c += 1) {
    let w = normalise(Float64Array.from({ length: d }, (_, i) => Math.sin(i + 1 + c * 7)));
    for (let iter = 0; iter < iterations; iter += 1) {
      const next = new Float64Array(d);
      residual.forEach((row) => {
        const projection = dot(row, w);
        for (let i = 0; i < d; i += 1) next[i] += projection * row[i];
      });
      w = normalise(next);
    }
    components.push(w);
    residual = residual.map((row) => {
      const projection = dot(row, w);
      return Float64Array.from({ length: d }, (_, i) => row[i] - projection * w[i]);
    });
  }

  return centred.map((row) => components.map((w) => dot(row, w)));
}

export function normalizeCoords(points) {
  if (points.length === 0) return [];
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  const spread = Math.max(
    Math.max(...xs) - Math.min(...xs),
    Math.max(...ys) - Math.min(...ys),
  ) || 1;
  const cx = (Math.max(...xs) + Math.min(...xs)) / 2;
  const cy = (Math.max(...ys) + Math.min(...ys)) / 2;
  return points.map(([x, y]) => [
    (2 * (x - cx)) / spread,
    (2 * (y - cy)) / spread,
  ]);
}
