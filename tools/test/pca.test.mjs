import test from 'node:test';
import assert from 'node:assert/strict';
import { pca2, normalizeCoords } from '../pca.mjs';

function embed3in6(points) {
  // Lift 2-D points into 6-D by a fixed linear map plus a constant offset.
  return points.map(([x, y]) => [x, y, 0.5 * x, -0.25 * y, 1, 1]);
}

test('pca2 returns one 2-D coordinate per input vector', () => {
  const out = pca2(embed3in6([[0, 0], [1, 0], [0, 1], [1, 1]]));
  assert.equal(out.length, 4);
  out.forEach((point) => assert.equal(point.length, 2));
});

test('pca2 is deterministic across runs', () => {
  const data = embed3in6([[0, 0], [2, 1], [-1, 3], [4, -2], [1, 1]]);
  assert.deepEqual(pca2(data), pca2(data));
});

test('pca2 preserves the relative spread of well-separated clusters', () => {
  const cluster = [[0, 0], [0.1, 0.1], [-0.1, 0], [10, 10], [10.1, 9.9], [9.9, 10]];
  const out = pca2(embed3in6(cluster));
  const within = Math.hypot(out[0][0] - out[1][0], out[0][1] - out[1][1]);
  const between = Math.hypot(out[0][0] - out[3][0], out[0][1] - out[3][1]);
  assert.ok(between > within * 5, `between=${between} within=${within}`);
});

test('normalizeCoords maps everything into [-1, 1]', () => {
  const out = normalizeCoords([[0, 0], [50, -30], [-10, 90]]);
  out.forEach(([x, y]) => {
    assert.ok(x >= -1 && x <= 1, `x=${x}`);
    assert.ok(y >= -1 && y <= 1, `y=${y}`);
  });
});

test('normalizeCoords touches both extremes on the widest axis', () => {
  const out = normalizeCoords([[0, 0], [10, 1], [-10, -1]]);
  const xs = out.map((point) => point[0]);
  assert.ok(Math.abs(Math.min(...xs) + 1) < 1e-9);
  assert.ok(Math.abs(Math.max(...xs) - 1) < 1e-9);
});

test('normalizeCoords survives a degenerate single point', () => {
  const out = normalizeCoords([[5, 5]]);
  assert.equal(out.length, 1);
  assert.ok(Number.isFinite(out[0][0]) && Number.isFinite(out[0][1]));
});
