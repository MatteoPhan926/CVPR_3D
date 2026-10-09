#!/usr/bin/env python3
"""Read-only auth/resource preflight; never prints credentials or starts a GPU job."""
import argparse, glob, json, os, shutil
from datetime import datetime, timezone
from pathlib import Path
from huggingface_hub import HfApi, get_token

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args()
dest = Path(args.output)
if dest.exists(): raise SystemExit('Refusing to overwrite an existing access record')
names = ['HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN', 'HUGGINGFACEHUB_API_TOKEN',
         'FAL_KEY', 'REPLICATE_API_TOKEN', 'MESHY_API_KEY', 'TRIPO_API_KEY', 'RUNPOD_API_KEY']
result = {'utc': datetime.now(timezone.utc).isoformat(),
          'operation': 'read-only official HfApi.whoami and local resource/name presence checks',
          'credential_variable_presence': {k: bool(os.environ.get(k)) for k in names},
          'nvidia_devices': glob.glob('/dev/nvidia*'), 'nvidia_smi': shutil.which('nvidia-smi'),
          'gpu_generation_requests': 0, 'upload_requests': 0, 'credential_values_logged': False}
token = get_token()
result['hf_default_token_resolves'] = bool(token)
if token:
    try:
        account = HfApi(token=token).whoami()
        result['auth'] = {'http_status': 200, 'identity_returned': bool(account.get('id') or account.get('name')),
                          'identity_recorded': False}
    except Exception as exc:
        response = getattr(exc, 'response', None)
        auth = {'http_status': getattr(response, 'status_code', None), 'error_class': type(exc).__name__,
                'identity_returned': False, 'provider_error': 'Body omitted outside safe diagnostic allowlist.'}
        if response is not None:
            try:
                msg = response.json().get('error', '')
                if msg in ['Invalid username or password.', 'Invalid user token.',
                           'Invalid credentials in Authorization header',
                           'Invalid credentials in Authorization header.', 'Invalid token', 'Invalid token.']:
                    auth['provider_error'] = msg
            except Exception:
                pass
        result['auth'] = auth
else:
    result['auth'] = {'status': 'not_called_no_token', 'identity_returned': False}
result['authentication_usable'] = result['auth'].get('http_status') == 200 and result['auth']['identity_returned']
result['gpu_admission_verified'] = False
result['interpretation'] = 'Authentication alone does not establish GPU admission; auth failure does not isolate token contents from proxy/binding propagation.'
with dest.open('x') as f: json.dump(result, f, indent=2)
print(json.dumps(result, indent=2))
