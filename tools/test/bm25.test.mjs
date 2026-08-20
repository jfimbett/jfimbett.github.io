import test from 'node:test';
import assert from 'node:assert/strict';
import { tokenize, buildIndex, search } from '../../assets/js/bm25.js';

const DOCS = [
  { id: 'bank-run', text: 'Social Media as a Bank Run Catalyst. Twitter exposure predicted deposit outflows at regional banks.' },
  { id: 'fund-flows', text: 'Tweeting for Money. Social media activity and mutual fund flows.' },
  { id: 'energy', text: 'Stroke of a Pen. Investment and stock returns under energy policy uncertainty.' },
];

test('tokenize lowercases, strips punctuation and drops stopwords', () => {
  const tokens = tokenize('The Bank, of England!');
  assert.ok(tokens.includes('bank'));
  assert.ok(tokens.includes('england'));
  assert.ok(!tokens.includes('the'));
  assert.ok(!tokens.includes('of'));
});

test('tokenize folds accents', () => {
  assert.deepEqual(tokenize('Université'), ['universite']);
});

test('search ranks the obviously relevant document first', () => {
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'bank run deposit')[0].id, 'bank-run');
  assert.equal(search(index, 'mutual fund flows')[0].id, 'fund-flows');
  assert.equal(search(index, 'energy policy uncertainty')[0].id, 'energy');
});

test('search returns nothing for an empty or stopword-only query', () => {
  const index = buildIndex(DOCS);
  assert.deepEqual(search(index, ''), []);
  assert.deepEqual(search(index, 'the of and'), []);
});

test('search returns nothing when no term matches', () => {
  const index = buildIndex(DOCS);
  assert.deepEqual(search(index, 'photosynthesis chlorophyll'), []);
});

test('rarer terms outrank common ones', () => {
  // "social" appears in two documents, "catalyst" in one.
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'catalyst')[0].id, 'bank-run');
  assert.equal(search(index, 'catalyst').length, 1);
});

test('results are sorted by descending score', () => {
  const index = buildIndex(DOCS);
  const results = search(index, 'social media');
  for (let i = 1; i < results.length; i += 1) {
    assert.ok(results[i - 1].score >= results[i].score);
  }
});

test('limit is respected', () => {
  const index = buildIndex(DOCS);
  assert.equal(search(index, 'social media', { limit: 1 }).length, 1);
});

test('an empty corpus returns no results and does not throw', () => {
  const index = buildIndex([]);
  assert.equal(index.N, 0);
  assert.equal(index.avgdl, 0);
  assert.deepEqual(search(index, 'anything'), []);
});

test('a corpus that tokenises to nothing returns no results and does not throw', () => {
  // Every document is stopwords only, so avgdl is 0 while N is 2 — the
  // degenerate shape most likely to produce NaN or Infinity scores.
  //
  // Note: this does NOT exercise the `index.avgdl || 1` guard in search().
  // That branch is unreachable by construction: avgdl === 0 implies every
  // tf map is empty, so the `if (!freq) return` early-exit fires before the
  // division is ever evaluated. The guard is retained as protection against
  // a future refactor that moves that early-exit, not because any input
  // reaches it today. Verified by instrumenting the branch: it never runs.
  const index = buildIndex([{ id: 'a', text: 'the and of' }, { id: 'b', text: 'it is at' }]);
  assert.equal(index.N, 2);
  assert.equal(index.avgdl, 0);
  assert.deepEqual(search(index, 'the bank'), []);
});
