import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const validator = require('gltf-validator');
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const output = process.argv[2] || path.join(here, 'verification/final/gltf_validation.json');
const results = {};
for (const [label, relativePath] of [['raw', 'raw/car_raw.glb'], ['authored', 'artifacts/car_authored.glb']]) {
  const bytes = fs.readFileSync(path.join(root, relativePath));
  const report = await validator.validateBytes(new Uint8Array(bytes), { uri: relativePath, maxIssues: 1000 });
  results[label] = { path: relativePath, sha256: crypto.createHash('sha256').update(bytes).digest('hex'), report };
}
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, JSON.stringify(results, null, 2) + '\n');
console.log(JSON.stringify(Object.fromEntries(Object.entries(results).map(([label, result]) => [label, { sha256: result.sha256, issues: result.report.issues }]))));
if (Object.values(results).some(result => result.report.issues.numErrors)) process.exitCode = 1;
