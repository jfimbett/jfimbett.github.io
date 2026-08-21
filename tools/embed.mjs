/**
 * Precompute paper embeddings and the hero's 2-D layout.
 *
 * Run from tools/:  npm run embed
 *
 * MODEL_ID is the single source of truth for which model is used. The browser
 * loads the same identifier in assets/js/semantic.js. If these two ever
 * diverge, similarity scores become meaningless without any visible error, so
 * changing one means changing the other.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { pipeline } from '@huggingface/transformers';
import { pca2, normalizeCoords } from './pca.mjs';

export const MODEL_ID = 'Xenova/all-MiniLM-L6-v2';

const DATA = new URL('../assets/data/', import.meta.url);

const round = (value) => Math.round(value * 10000) / 10000;

async function main() {
  const payload = JSON.parse(await readFile(new URL('search.json', DATA), 'utf8'));
  const docs = payload.docs;
  console.log(`Embedding ${docs.length} papers with ${MODEL_ID}…`);

  const extractor = await pipeline('feature-extraction', MODEL_ID);

  const vectors = [];
  for (const doc of docs) {
    const output = await extractor(doc.text, { pooling: 'mean', normalize: true });
    vectors.push(Array.from(output.data));
    console.log(`  ${doc.id}`);
  }

  const embeddings = {
    model: MODEL_ID,
    dims: vectors[0].length,
    vectors: Object.fromEntries(
      docs.map((doc, i) => [doc.id, vectors[i].map(round)]),
    ),
  };
  await writeFile(
    new URL('embeddings.json', DATA),
    JSON.stringify(embeddings, null, 1),
    'utf8',
  );

  const coords = normalizeCoords(pca2(vectors));
  const hero = {
    model: MODEL_ID,
    anchors: docs.map((doc, i) => ({
      id: doc.id,
      x: round(coords[i][0]),
      y: round(coords[i][1]),
      label: doc.short,
      title: doc.title,
      agenda: doc.agenda,
      href: `research.html#${doc.id}`,
    })),
  };
  await writeFile(new URL('hero.json', DATA), JSON.stringify(hero, null, 1), 'utf8');

  console.log(`Wrote embeddings.json (${embeddings.dims} dims) and hero.json`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
