/**
 * Paper entries: the stacked <details> blocks (summary, abstract, media…)
 * become a single row of toggles with one shared panel beneath, so an entry
 * takes one line until the reader opens something. Only one panel is open at
 * a time. Without JavaScript the <details> render as they are, and their
 * shared `name` attribute keeps one open at a time natively.
 *
 * A classic script, not a module, so it also runs when the page is opened
 * straight from disk (browsers block module scripts on file:// URLs).
 */
(function () {
function enhance(group, groupIndex) {
  const panels = Array.from(group.querySelectorAll(':scope > details'));
  if (panels.length === 0) return;

  const row = document.createElement('div');
  row.className = 'entry__tabs';

  const buttons = panels.map((details, i) => {
    const summary = details.querySelector(':scope > summary');
    const id = details.id || `panel-${groupIndex}-${i}`;
    details.id = id;
    details.open = false;

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'entry__tab';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', id);
    button.textContent = summary ? summary.textContent.trim() : `Panel ${i + 1}`;
    button.addEventListener('click', () => select(details.open ? -1 : i));
    row.appendChild(button);
    return button;
  });

  function select(index) {
    panels.forEach((details, i) => {
      const on = i === index;
      details.open = on;
      buttons[i].setAttribute('aria-expanded', String(on));
    });
  }

  group.classList.add('is-tabbed');
  group.insertBefore(row, group.firstChild);
}

document.querySelectorAll('.entry__panels').forEach(enhance);
})();
