/**
 * Hero: a curl-noise particle field whose anchor points are this site's
 * papers, positioned by PCA over their embeddings (assets/data/hero.json).
 *
 * The field periodically relaxes so drifting particles settle toward the
 * anchors, then resumes drifting.
 */

const canvas = document.getElementById('hero-canvas');
const label = document.getElementById('hero-label');

const GRENAT = [95, 25, 55];
const CORAL = [255, 110, 110];

function mix(a, b, t) {
  return `rgb(${Math.round(a[0] + (b[0] - a[0]) * t)},` +
         `${Math.round(a[1] + (b[1] - a[1]) * t)},` +
         `${Math.round(a[2] + (b[2] - a[2]) * t)})`;
}

/** Cheap, seeded value noise. No dependency, and stable across reloads. */
function noise(x, y, t) {
  return (
    Math.sin(x * 1.7 + t) * Math.cos(y * 1.3 - t * 0.7) +
    Math.sin((x + y) * 0.9 + t * 1.3) * 0.5
  );
}

async function start(target) {
  const context = target.getContext('2d', { alpha: false });
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let anchors = [];
  try {
    const response = await fetch('assets/data/hero.json');
    anchors = (await response.json()).anchors || [];
  } catch (error) {
    anchors = []; // The field still renders; it simply has no anchors.
  }

  let width = 0;
  let height = 0;
  let particles = [];

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    const rect = target.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    target.width = Math.round(width * ratio);
    target.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    const count = Math.min(2600, Math.round((width * height) / 260));
    particles = Array.from({ length: count }, (_, i) => ({
      // Deterministic placement: a golden-angle spiral, not Math.random,
      // so the first painted frame is identical on every load.
      x: (0.5 + 0.45 * Math.cos(i * 2.39996) * Math.sqrt(i / count)) * width,
      y: (0.5 + 0.45 * Math.sin(i * 2.39996) * Math.sqrt(i / count)) * height,
      vx: 0,
      vy: 0,
    }));
  }

  const toScreen = (anchor) => ({
    x: (anchor.x * 0.42 + 0.5) * width,
    y: (anchor.y * 0.42 + 0.5) * height,
  });

  const styles = getComputedStyle(document.documentElement);
  const background = styles.getPropertyValue('--grenat-pastel').trim() || '#ECE4E7';

  function frame(time) {
    const t = time * 0.00012;
    // Cycles between drifting (0) and gathering toward anchors (1).
    const gather = Math.max(0, Math.sin(t * 0.6)) ** 3;

    context.fillStyle = background;
    context.fillRect(0, 0, width, height);

    const screenAnchors = anchors.map(toScreen);

    particles.forEach((particle) => {
      const nx = particle.x / width;
      const ny = particle.y / height;
      let ax = noise(nx * 3, ny * 3, t) * 0.06;
      let ay = noise(ny * 3 + 5.2, nx * 3 - 2.1, t) * 0.06;

      if (gather > 0.01 && screenAnchors.length) {
        let best = screenAnchors[0];
        let bestDistance = Infinity;
        screenAnchors.forEach((anchor) => {
          const distance = (anchor.x - particle.x) ** 2 + (anchor.y - particle.y) ** 2;
          if (distance < bestDistance) { bestDistance = distance; best = anchor; }
        });
        ax += ((best.x - particle.x) / width) * gather * 0.9;
        ay += ((best.y - particle.y) / height) * gather * 0.9;
      }

      particle.vx = (particle.vx + ax) * 0.94;
      particle.vy = (particle.vy + ay) * 0.94;
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x < 0) particle.x += width;
      if (particle.x > width) particle.x -= width;
      if (particle.y < 0) particle.y += height;
      if (particle.y > height) particle.y -= height;

      const speed = Math.min(1, Math.hypot(particle.vx, particle.vy) * 6);
      context.fillStyle = mix(GRENAT, CORAL, speed);
      context.globalAlpha = 0.35 + speed * 0.45;
      context.fillRect(particle.x, particle.y, 1.4, 1.4);
    });

    context.globalAlpha = 1;
    screenAnchors.forEach((anchor) => {
      context.beginPath();
      context.arc(anchor.x, anchor.y, 4.5, 0, Math.PI * 2);
      context.fillStyle = mix(GRENAT, CORAL, 0.25);
      context.fill();
    });
  }

  let running = false;
  let handle = 0;

  function loop(time) {
    frame(time);
    handle = requestAnimationFrame(loop);
  }

  function play() {
    if (running || reduced) return;
    running = true;
    handle = requestAnimationFrame(loop);
  }

  function pause() {
    running = false;
    cancelAnimationFrame(handle);
  }

  resize();
  frame(0);

  let intersecting = false;

  function updatePlayState() {
    // Two independent signals (viewport visibility and tab visibility) drive
    // one loop. Both must be satisfied, or a tab switch can resume the loop
    // on a hero that is scrolled far off-screen.
    if (intersecting && !document.hidden) {
      play();
    } else {
      pause();
    }
  }

  if (!reduced) {
    window.addEventListener('resize', () => { resize(); });
    new IntersectionObserver((entries) => {
      intersecting = entries[0].isIntersecting;
      updatePlayState();
    }).observe(target);
    document.addEventListener('visibilitychange', updatePlayState);
  }

  // Anchor hover and click.
  target.addEventListener('mousemove', (event) => {
    const rect = target.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;
    const hit = anchors.find((anchor) => {
      const point = toScreen(anchor);
      return Math.hypot(point.x - mx, point.y - my) < 14;
    });
    if (hit) {
      label.textContent = hit.label;
      label.style.left = `${mx + 12}px`;
      label.style.top = `${my - 8}px`;
      label.dataset.visible = 'true';
      target.style.cursor = 'pointer';
    } else {
      label.dataset.visible = 'false';
      target.style.cursor = 'default';
    }
  });

  target.addEventListener('click', (event) => {
    const rect = target.getBoundingClientRect();
    const mx = event.clientX - rect.left;
    const my = event.clientY - rect.top;
    const hit = anchors.find((anchor) => {
      const point = toScreen(anchor);
      return Math.hypot(point.x - mx, point.y - my) < 14;
    });
    if (hit) window.location.href = hit.href;
  });
}

// Kick off last: start() closes over GRENAT and CORAL, which are in the
// temporal dead zone until this point in the module.
if (canvas && canvas.getContext) {
  start(canvas);
}
