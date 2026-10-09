// Explicit input/output only; no inherited hard-coded car targets or external fetches.
const fs = require('fs');
const crypto = require('crypto');
const validator = require('/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules/gltf-validator');
const [input, output] = process.argv.slice(2);
if (!input || !output || fs.existsSync(output)) throw new Error('Need input and a new output path');
const bytes = fs.readFileSync(input);
validator.validateBytes(new Uint8Array(bytes), {uri:input, maxIssues:100,
  externalResourceFunction:uri=>Promise.reject(new Error('External resource not allowed: '+uri))
}).then(report=>{
  report.evidence = {input, sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
    validator_version:validator.version(), no_external_resources:true,
    scope:'GLB container/schema validation only; not model provenance, appearance or task success'};
  fs.writeFileSync(output, JSON.stringify(report,null,2),{flag:'wx'});
  console.log(JSON.stringify({errors:report.issues.numErrors,warnings:report.issues.numWarnings,
    infos:report.issues.numInfos,hints:report.issues.numHints}));
  process.exitCode = report.issues.numErrors ? 1 : 0;
}).catch(error=>{console.error(error);process.exitCode=1;});
