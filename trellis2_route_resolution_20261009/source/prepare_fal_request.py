#!/usr/bin/env python3
"""Offline request preparation and schema verification. Contains no network calls."""
import base64, hashlib, json
from pathlib import Path
import jsonschema

root = Path(__file__).resolve().parents[1]
original = (root / 'inputs/original.jpg').read_bytes()
assert hashlib.sha256(original).hexdigest() == 'b5b9ed4aece1359a0d291e89149634499583102e27f177aadb4c60f327e996e1'
plan = json.loads((root / 'config/PREVIOUS_GENERATION_PLAN.json').read_text())
schema_bytes = (root / 'research/commercial_routes/review/fal_schema.json').read_bytes()
schema = json.loads(schema_bytes)['components']['schemas']['Trellis2Input']
payload = {key: prop['default'] for key, prop in schema['properties'].items() if 'default' in prop}
payload.update(seed=plan['seed'], resolution=int(plan['resolution']), **plan['generation_parameters'], **plan['export_parameters'])
payload['image_url'] = 'data:image/jpeg;base64,' + base64.b64encode(original).decode()
assert set(payload) <= set(schema['properties'])
jsonschema.validate(payload, schema)
for stage in ['ss', 'shape_slat', 'tex_slat']:
    assert payload[stage+'_guidance_interval_start'] <= payload[stage+'_guidance_interval_end']
assert base64.b64decode(payload['image_url'].split(',',1)[1], validate=True) == original
# Verify that a tempting UI string value fails the actual API integer enum.
bad = dict(payload, resolution='1024')
try:
    jsonschema.validate(bad, schema)
except jsonschema.ValidationError:
    rejects_ui_string_resolution = True
else:
    raise AssertionError('Expected strict resolution type rejection')
output = root / 'config/fal_request_prepared_NOT_SUBMITTED.json'
with output.open('x') as f: json.dump(payload, f, indent=2)
record = {'status': 'offline_schema_checked_not_submitted', 'network_calls': 0,
    'endpoint': 'fal-ai/trellis-2', 'request_file': str(output.relative_to(root)),
    'request_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'schema_sha256': hashlib.sha256(schema_bytes).hexdigest(),
    'input_sha256': hashlib.sha256(original).hexdigest(),
    'encoded_input_roundtrip_exact': True, 'rejects_string_resolution': rejects_ui_string_resolution,
    'inherited_controls': ['seed','resolution',*plan['generation_parameters'],*plan['export_parameters']],
    'field_count': len(payload), 'advertised_cost_usd': 0.30, 'paid_execution_authorized': False,
    'provenance_change': 'Original JPEG preserved; fal preprocessing/model revision and export implementation are unverified; no exact Microsoft Space reproduction claim.',
    'required_before_submission': ['Explicit authorization for one paid fal request and cost ceiling',
        'Valid securely bound FAL_KEY and sufficient balance; minimum account top-up unknown',
        'Recheck resolution-specific price and service schema',
        'Verify current external input/config/code checkpoint',
        'New exclusive request directory, save request ID, never resubmit on unknown timeout',
        'Download complete returned GLB and preserve bytes before DCC use'],
    'limits': 'Static schema checking does not validate provider execution, preprocessing, pricing charged or output quality.'}
with (root / 'research/fal_request_preparation.json').open('x') as f: json.dump(record, f, indent=2)
print(json.dumps(record, indent=2))
