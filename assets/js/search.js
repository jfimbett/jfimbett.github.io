/**
 * Site search. Tier 1: BM25 over a ~30KB index, fetched on first open.
 * Task 9 upgrades ranking in place by replacing window.__searchRerank.
 */
import { buildIndex, search } from './bm25.js';

const state = { index: null, docs: null, open: false, loading: false };
let runToken = 0;

window.__searchRerank = null;

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === 'class') node.className = value;
    else if (key === 'text') node.textContent = value;
    else node.setAttribute(key, value);
  });
  children.forEach((child) => node.appendChild(child));
  return node;
}

const dialog = el('div', {
  class: 'search', id: 'search', role: 'dialog',
  'aria-modal': 'true', 'aria-label': 'Search this site', hidden: '',
});
const input = el('input', {
  class: 'search__input', type: 'search', id: 'search-input',
  placeholder: 'Ask a question, or search by keyword…',
  autocomplete: 'off', role: 'combobox', 'aria-expanded': 'false',
  'aria-controls': 'search-results', 'aria-autocomplete': 'list',
});
const results = el('ul', { class: 'search__results', id: 'search-results', role: 'listbox' });
const status = el('p', { class: 'search__status', role: 'status', 'aria-live': 'polite' });
dialog.append(el('div', { class: 'search__panel' }, [input, status, results]));
document.body.appendChild(dialog);

let active = -1;

function render(hits) {
  results.textContent = '';
  active = -1;
  hits.forEach((hit, i) => {
    const doc = state.docs.get(hit.id);
    const link = el('a', { href: 'research.html#' + doc.id, tabindex: '-1' });
    link.appendChild(el('span', { class: 'search__title', text: doc.title }));
    link.appendChild(el('span', { class: 'search__meta', text: doc.venue }));
    const item = el('li', { class: 'search__result', role: 'option', id: 'search-opt-' + i, 'aria-selected': 'false' }, [link]);
    results.appendChild(item);
  });
  input.setAttribute('aria-expanded', hits.length ? 'true' : 'false');
  status.textContent = hits.length
    ? hits.length + (hits.length === 1 ? ' result' : ' results')
    : (input.value.trim() ? 'No results' : '');
}

function highlight(next) {
  const items = [...results.children];
  if (!items.length) return;
  if (active >= 0) items[active].setAttribute('aria-selected', 'false');
  active = (next + items.length) % items.length;
  items[active].setAttribute('aria-selected', 'true');
  items[active].scrollIntoView({ block: 'nearest' });
  input.setAttribute('aria-activedescendant', items[active].id);
}

async function ensureIndex() {
  if (state.index || state.loading) return;
  state.loading = true;
  status.textContent = 'Loading…';
  try {
    const response = await fetch('assets/data/search.json');
    const payload = await response.json();
    state.docs = new Map(payload.docs.map((doc) => [doc.id, doc]));
    state.index = buildIndex(payload.docs);
    status.textContent = '';
    if (window.__loadSemantic) window.__loadSemantic();
  } catch (error) {
    status.textContent = 'Search is unavailable.';
  } finally {
    state.loading = false;
  }
}

async function run() {
  if (!state.index) return;
  const token = ++runToken;
  const query = input.value.trim();
  if (!query) { render([]); return; }

  let hits = search(state.index, query, { limit: 8 });
  if (window.__searchRerank) {
    try {
      const reranked = await window.__searchRerank(query, hits, state.docs);
      // A newer query started while we awaited: drop this result entirely
      // rather than rendering it over fresher output.
      if (token !== runToken) return;
      hits = reranked;
    } catch (error) {
      if (token !== runToken) return;
      /* Tier 1 results stand. */
    }
  }
  if (token !== runToken) return;
  render(hits);
}

function open() {
  state.open = true;
  dialog.hidden = false;
  document.getElementById('search-open').setAttribute('aria-expanded', 'true');
  input.focus();
  ensureIndex();
}

function close() {
  state.open = false;
  dialog.hidden = true;
  const button = document.getElementById('search-open');
  button.setAttribute('aria-expanded', 'false');
  button.focus();
}

document.getElementById('search-open').addEventListener('click', open);
dialog.addEventListener('click', (event) => { if (event.target === dialog) close(); });

let timer;
input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 90); });

input.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowDown') { event.preventDefault(); highlight(active + 1); }
  else if (event.key === 'ArrowUp') { event.preventDefault(); highlight(active - 1); }
  else if (event.key === 'Enter' && active >= 0) {
    event.preventDefault();
    results.children[active].querySelector('a').click();
  } else if (event.key === 'Escape') { close(); }
  else if (event.key === 'Tab') {
    // aria-modal promises background content is unreachable, and the
    // combobox pattern requires DOM focus to stay on the input while
    // aria-activedescendant moves the virtual selection. Results are
    // reachable via the arrow keys and Enter, so Tab has nothing to move to.
    event.preventDefault();
  }
});

document.addEventListener('keydown', (event) => {
  const active = document.activeElement;
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(active.tagName) || active.isContentEditable;
  if (event.key === '/' && !state.open && !typing) { event.preventDefault(); open(); }
  else if (event.key === 'Escape' && state.open) { close(); }
});
