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

test('empty corpus does not divide by zero', () => {
  const index = buildIndex([]);
  assert.equal(index.N, 0);
  assert.equal(index.avgdl, 0);
  assert.deepEqual(search(index, 'anything'), []);
});

test('a corpus of only stopwords does not divide by zero', () => {
  // Every document tokenises to nothing, so avgdl is 0 while N is 2.
  const index = buildIndex([{ id: 'a', text: 'the and of' }, { id: 'b', text: 'it is at' }]);
  assert.equal(index.avgdl, 0);
  assert.deepEqual(search(index, 'the bank'), []);
});
