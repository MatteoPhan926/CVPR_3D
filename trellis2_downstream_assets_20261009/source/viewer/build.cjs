#!/usr/bin/env node
'use strict';
// Explicit existing GLB input only. No network, waiting, or inherited asset paths.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const dependencies = '/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules';
const esbuild = require(path.join(dependencies, 'esbuild'));
const flags = process.argv.slice(2);
function option(name) { const i = flags.indexOf(name); if (i < 0 || !flags[i + 1]) throw Error(`Required ${name}`); return flags[i + 1]; }
const input = path.resolve(option('--input'));
const output = path.resolve(option('--output'));
if (!fs.existsSync(input)) throw Error(`GLB input must already exist: ${input}`);
if (fs.existsSync(output)) throw Error(`Refusing to replace existing viewer: ${output}`);
const data = fs.readFileSync(input);
if (data.toString('ascii', 0, 4) !== 'glTF' || data.readUInt32LE(4) !== 2 || data.readUInt32LE(8) !== data.length) throw Error('Invalid GLB container');
const threeVersion = JSON.parse(fs.readFileSync(path.join(dependencies, 'three/package.json'))).version;
if (threeVersion !== '0.170.0') throw Error(`Unexpected Three.js version: ${threeVersion}`);
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const metadata = { assetFile: path.basename(input), assetBytes: data.length, assetSha256: sha256(data),
  originalSource: 'sample_2026-10-09T183055.354.glb', sourceAssociation: 'Supplied HF-direct asset A; resolution mapping unknown',
  authoring: 'Native exterior partition; moving door; labelled lining, edge, jamb and proxy cabin additions',
  threeVersion, esbuildVersion: esbuild.version, buildUtc: new Date().toISOString() };
const result = esbuild.buildSync({ entryPoints: [path.join(__dirname, 'main.js')], bundle: true, minify: true,
  write: false, format: 'iife', platform: 'browser', target: ['es2020'], nodePaths: [dependencies], legalComments: 'inline' });
const bundle = result.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');
const license = fs.readFileSync(path.join(dependencies, 'three/LICENSE'), 'utf8');
let html = fs.readFileSync(path.join(__dirname, 'template.html'), 'utf8');
html = html.replace('__METADATA__', JSON.stringify(metadata).replace(/</g, '\\u003c'))
  .replace('__ASSET_BASE64__', data.toString('base64')).replace('__BUNDLE__', () => bundle)
  .replace('__THIRD_PARTY_LICENSE__', license);
if (Buffer.byteLength(html) >= 50 * 1024 * 1024) throw Error('Standalone HTML exceeds the 50 MiB budget');
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, html, { flag: 'wx' });
const record = { ...metadata, input, output, outputBytes: Buffer.byteLength(html), outputSha256: sha256(html),
  bundleBytes: Buffer.byteLength(bundle), externalResourcesRequired: false,
  scope: 'Built artifact only. Browser operation, material appearance and animation require verification.' };
fs.writeFileSync(output.replace(/\.html$/, '') + '.build.json', JSON.stringify(record, null, 2), { flag: 'wx' });
console.log(JSON.stringify(record, null, 2));
