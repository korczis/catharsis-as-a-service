// Copies the pinned browser bundles out of node_modules so the site self-hosts them (no CDN).
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const TARGET = join(ROOT, 'static/js/vendor');
const BUNDLES = {
  'alpine.min.js': 'node_modules/alpinejs/dist/cdn.min.js',
  'flowbite.min.js': 'node_modules/flowbite/dist/flowbite.min.js',
};

mkdirSync(TARGET, { recursive: true });
for (const [name, source] of Object.entries(BUNDLES)) {
  copyFileSync(join(ROOT, source), join(TARGET, name));
  console.log(`vendor ${source} -> static/js/vendor/${name}`);
}
