/**
 * Research map: a labelled scatter of this site's papers in embedding space.
 *
 * Points come from assets/data/hero.json — a 2-D PCA projection of the paper
 * embeddings computed in tools/embed.mjs. Colour is the paper's research
 * agenda; the matching legend and an equivalent list of links are in the HTML,
 * so nothing here is the only route to the content.
 *
 * There is no animation loop. The points ease in once when the figure first
 * scrolls into view, and after that the canvas repaints only when something
 * actually changes: hover, focus, or a resize.
 */

const canvas = document.getElementById('plot-canvas');
const tooltip = document.getElementById('plot-tooltip');

const ENTRANCE_MS = 700;
const STAGGER_MS = 45;
const BASE_POINT_R = 6;
const BASE_LABEL_PX = 13;
/** Pointer distance, in CSS pixels, that still counts as hitting a point. */
const HIT_SLOP = 22;
const COARSE_HIT_SLOP = 30;

const easeOut = (t) => 1 - (1 - t) ** 3;
const clamp = (value, low, high) => Math.min(high, Math.max(low, value));

/**
 * Marker shape per agenda. Two of the four series are in the same red family,
 * and colour alone also fails for red-green colour blindness, so shape carries
 * the distinction too. The legend swatches in site.css mirror these shapes.
 */
const SHAPES = {
  'social-media': 'circle',
  'corporate-finance': 'square',
  'asset-pricing': 'triangle',
  'computational-finance': 'diamond',
};

function markerPath(context, shape, x, y, r) {
  context.beginPath();
  if (shape === 'square') {
    const side = r * 1.75;
    context.rect(x - side / 2, y - side / 2, side, side);
  } else if (shape === 'triangle') {
    const size = r * 1.25;
    context.moveTo(x, y - size);
    context.lineTo(x + size * 0.95, y + size * 0.8);
    context.lineTo(x - size * 0.95, y + size * 0.8);
    context.closePath();
  } else if (shape === 'diamond') {
    const size = r * 1.25;
    context.moveTo(x, y - size);
    context.lineTo(x + size, y);
    context.lineTo(x, y + size);
    context.lineTo(x - size, y);
    context.closePath();
  } else {
    context.arc(x, y, r, 0, Math.PI * 2);
  }
}

/** Label offsets tried in order; the first collision-free one wins. */
const LABEL_PLACEMENTS = [
  { dx: 1, dy: 0, align: 'left', baseline: 'middle' },
  { dx: -1, dy: 0, align: 'right', baseline: 'middle' },
  { dx: 0, dy: -1, align: 'center', baseline: 'bottom' },
  { dx: 0, dy: 1, align: 'center', baseline: 'top' },
];

function overlaps(a, b) {
  return !(a.right < b.left || a.left > b.right || a.bottom < b.top || a.top > b.bottom);
}

async function start(target) {
  const context = target.getContext('2d');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarse = window.matchMedia('(pointer: coarse)').matches;

  let anchors = [];
  try {
    const response = await fetch('assets/data/hero.json');
    anchors = (await response.json()).anchors || [];
  } catch (error) {
    return; // No data, no chart. The figcaption list still lists every paper.
  }
  if (!anchors.length) return;

  const styles = getComputedStyle(document.documentElement);
  const token = (name, fallback) =>
    styles.getPropertyValue(name).trim() || fallback;

  const paper = token('--paper', '#FFFFFF');
  const ink = token('--ink', '#0E0E0E');
  const grid = token('--border', '#DCDCDC');
  const muted = token('--muted', '#5A5A5A');
  // Canvas has no access to CSS custom properties, so the font stack is
  // resolved here rather than written as var(--body).
  const bodyFont = token('--body', 'sans-serif');
  const colourOf = (anchor) =>
    token(`--plot-${anchor.agenda}`, token('--grenat', '#5F1937'));

  let width = 0;
  let height = 0;
  let points = [];
  /** Labels are drawn only when there is room for them to stay readable. */
  let showLabels = true;
  let hovered = -1;
  // Point and type size follow the canvas so the chart keeps the same visual
  // weight on a laptop and on a wide monitor.
  let pointR = BASE_POINT_R;
  let labelPx = BASE_LABEL_PX;

  function layout() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    const rect = target.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    target.width = Math.round(width * ratio);
    target.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    showLabels = width >= 620;
    // Without labels the markers carry the whole chart and are touch targets,
    // so they get a floor of their own.
    const gain = clamp(width / 900, showLabels ? 0.9 : 1.2, 1.3);
    pointR = BASE_POINT_R * gain;
    labelPx = Math.round(BASE_LABEL_PX * gain);

    // Room for labels on the sides; less is needed when they are suppressed.
    const padX = showLabels ? clamp(width * 0.17, 60, 150) : 26;
    const padY = showLabels ? clamp(height * 0.12, 30, 70) : 26;

    points = anchors.map((anchor) => ({
      anchor,
      // hero.json coordinates are normalised to [-1, 1], y pointing up.
      x: padX + ((anchor.x + 1) / 2) * (width - padX * 2),
      y: padY + ((1 - anchor.y) / 2) * (height - padY * 2),
      colour: colourOf(anchor),
      shape: SHAPES[anchor.agenda] || 'circle',
    }));
  }

  function drawGrid() {
    context.strokeStyle = grid;
    context.lineWidth = 1;
    context.globalAlpha = 0.7;
    for (let i = 1; i < 4; i += 1) {
      const x = Math.round((width * i) / 4) + 0.5;
      const y = Math.round((height * i) / 4) + 0.5;
      context.beginPath();
      context.moveTo(x, 0);
      context.lineTo(x, height);
      context.stroke();
      context.beginPath();
      context.moveTo(0, y);
      context.lineTo(width, y);
      context.stroke();
    }
    context.globalAlpha = 1;
  }

  function drawAxisCaptions() {
    if (!showLabels) return;
    context.fillStyle = muted;
    context.font = `${labelPx - 2}px ${bodyFont}`;
    context.textAlign = 'right';
    context.textBaseline = 'bottom';
    context.fillText('component 1 →', width - 10, height - 8);
    context.save();
    context.translate(12, 10);
    context.rotate(-Math.PI / 2);
    context.textAlign = 'right';
    context.textBaseline = 'top';
    context.fillText('component 2 →', 0, 0);
    context.restore();
  }

  /**
   * Place each label in the first offset that clears every point and every
   * label already placed. Purely geometric, so the result is identical on
   * every load and every repaint.
   */
  function placeLabels(scales) {
    const placed = [];
    const halfLine = labelPx * 0.75;

    points.forEach((point, index) => {
      if (scales[index] <= 0) return;
      const text = point.anchor.label;
      const textWidth = context.measureText(text).width;
      const gap = pointR + 7;

      let chosen = null;
      for (const placement of LABEL_PLACEMENTS) {
        const cx = point.x + placement.dx * gap;
        const cy = point.y + placement.dy * (gap + halfLine * 0.4);
        const left = placement.align === 'left' ? cx
          : placement.align === 'right' ? cx - textWidth
            : cx - textWidth / 2;
        const top = placement.baseline === 'top' ? cy
          : placement.baseline === 'bottom' ? cy - halfLine * 2
            : cy - halfLine;
        const box = {
          left: left - 2, right: left + textWidth + 2,
          top: top - 2, bottom: top + halfLine * 2 + 2,
        };
        if (box.left < 2 || box.right > width - 2) continue;
        if (box.top < 2 || box.bottom > height - 2) continue;
        if (placed.some((other) => overlaps(box, other))) continue;
        const hitsPoint = points.some((other, j) => j !== index && overlaps(box, {
          left: other.x - pointR, right: other.x + pointR,
          top: other.y - pointR, bottom: other.y + pointR,
        }));
        if (hitsPoint) continue;
        chosen = { text, x: cx, y: cy, align: placement.align, baseline: placement.baseline, box };
        break;
      }
      if (!chosen) return; // Crowded corner: the point still carries a tooltip.
      placed.push(chosen.box);
      chosen.index = index;
      point.label = chosen;
    });
  }

  function draw(scales) {
    context.fillStyle = paper;
    context.fillRect(0, 0, width, height);
    drawGrid();
    drawAxisCaptions();

    context.font = `${labelPx}px ${bodyFont}`;
    points.forEach((point) => { point.label = null; });
    if (showLabels) placeLabels(scales);

    points.forEach((point, index) => {
      const scale = scales[index];
      if (scale <= 0) return;
      const isHovered = index === hovered;
      const radius = pointR * (isHovered ? 1.5 : 1) * scale;

      if (isHovered) {
        markerPath(context, point.shape, point.x, point.y, radius + 5);
        context.strokeStyle = point.colour;
        context.globalAlpha = 0.35;
        context.lineWidth = 2;
        context.stroke();
        context.globalAlpha = 1;
      }

      markerPath(context, point.shape, point.x, point.y, radius);
      context.fillStyle = point.colour;
      context.fill();
      // A ring in the canvas colour keeps neighbouring points distinct.
      context.lineWidth = 1.5;
      context.strokeStyle = paper;
      context.stroke();
    });

    points.forEach((point, index) => {
      if (!point.label) return;
      const label = point.label;
      context.textAlign = label.align;
      context.textBaseline = label.baseline;
      // Halo first, so a label crossing a gridline stays readable.
      context.lineWidth = 3;
      context.strokeStyle = paper;
      context.strokeText(label.text, label.x, label.y);
      context.fillStyle = index === hovered ? point.colour : ink;
      context.fillText(label.text, label.x, label.y);
    });
  }

  const fullScales = () => points.map(() => 1);

  function paintStatic() {
    draw(fullScales());
  }

  function animateEntrance() {
    const started = performance.now();
    const step = (now) => {
      const elapsed = now - started;
      const scales = points.map((_, index) =>
        easeOut(clamp((elapsed - index * STAGGER_MS) / ENTRANCE_MS, 0, 1)));
      draw(scales);
      if (elapsed < ENTRANCE_MS + points.length * STAGGER_MS) {
        requestAnimationFrame(step);
      } else {
        paintStatic();
      }
    };
    requestAnimationFrame(step);
  }

  function hit(clientX, clientY) {
    const rect = target.getBoundingClientRect();
    const mx = clientX - rect.left;
    const my = clientY - rect.top;
    const slop = coarse ? COARSE_HIT_SLOP : HIT_SLOP;
    let best = -1;
    let bestDistance = slop;
    points.forEach((point, index) => {
      const distance = Math.hypot(point.x - mx, point.y - my);
      if (distance < bestDistance) { bestDistance = distance; best = index; }
    });
    return { index: best, x: mx, y: my };
  }

  function showTooltip(index, x, y) {
    const point = points[index];
    tooltip.textContent = point.anchor.title || point.anchor.label;
    tooltip.style.left = `${clamp(x + 14, 0, Math.max(0, width - 40))}px`;
    tooltip.style.top = `${clamp(y - 10, 0, Math.max(0, height - 20))}px`;
    tooltip.dataset.visible = 'true';
  }

  function setHover(index, x, y) {
    if (index === hovered && index === -1) return;
    hovered = index;
    if (index === -1) {
      tooltip.dataset.visible = 'false';
      target.style.cursor = 'default';
    } else {
      showTooltip(index, x, y);
      target.style.cursor = 'pointer';
    }
    paintStatic();
  }

  layout();
  if (reduced) {
    paintStatic();
  } else {
    // Hold the first frame blank until the figure is actually on screen, so
    // the entrance is something the visitor sees rather than something that
    // has already finished by the time they scroll down.
    draw(points.map(() => 0));
    const observer = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      observer.disconnect();
      animateEntrance();
    }, { threshold: 0.25 });
    observer.observe(target);
  }

  let resizeHandle = 0;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(resizeHandle);
    resizeHandle = requestAnimationFrame(() => {
      layout();
      paintStatic();
    });
  });

  target.addEventListener('pointermove', (event) => {
    const found = hit(event.clientX, event.clientY);
    setHover(found.index, found.x, found.y);
  });

  target.addEventListener('pointerleave', () => setHover(-1, 0, 0));

  target.addEventListener('click', (event) => {
    const found = hit(event.clientX, event.clientY);
    if (found.index === -1) return;
    // On touch there is no hover: the first tap reveals the title, a second
    // tap on the same point opens the paper.
    if (coarse && hovered !== found.index) {
      setHover(found.index, found.x, found.y);
      return;
    }
    window.location.href = points[found.index].anchor.href;
  });

  target.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      event.preventDefault();
      const next = (hovered + 1) % points.length;
      setHover(next, points[next].x, points[next].y);
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      event.preventDefault();
      const next = (hovered <= 0 ? points.length : hovered) - 1;
      setHover(next, points[next].x, points[next].y);
    } else if (event.key === 'Enter' && hovered !== -1) {
      event.preventDefault();
      window.location.href = points[hovered].anchor.href;
    } else if (event.key === 'Escape') {
      setHover(-1, 0, 0);
    }
  });

  target.addEventListener('blur', () => setHover(-1, 0, 0));
}

if (canvas && canvas.getContext) {
  start(canvas);
}
