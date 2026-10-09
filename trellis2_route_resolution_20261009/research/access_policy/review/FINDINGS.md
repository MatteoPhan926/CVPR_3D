# Independent access-policy review — 2026-10-09

Scope: inspect saved public sources and exact deployed client distribution. No credentials were sent by this review, no GPU endpoints were called, no config or git state was changed, and no package was installed or executed. Only public PyPI metadata/wheel and one official Gradio documentation page were fetched with GET. Parent agent separately verifies current authentication.

## Concrete result

A specific client-side accounting mechanism can explain the reported `120s requested vs. 176s left`. It remains a supported hypothesis, not a verified account of the remote scheduler. The authenticated official route is documented and public, but no reviewed read-only operation can guarantee allocation for generation and subsequent export.

## Documented route and prerequisites

- Use the official public Space `microsoft/TRELLIS.2` / `https://microsoft-trellis-2.hf.space` with a valid Hugging Face User Access Token through the supported Gradio Python client. The official Gradio guide documents passing a token to `Client`; current guide uses `token=`, while client versions may use `hf_token=`. Match the installed client signature rather than copying a version-mismatched keyword. The token docs say read tokens are appropriate for read/inference, with fine-grained resource scopes also available; write permission is not established as necessary.
- Validate the existing supported binding with official `HfApi.whoami` before claiming authenticated access. The saved `../../auth_official_client.json` records an injected binding resolving but HTTP 401, with no authenticated identity returned at 09:05:50 UTC. That proves that request failed; it does not isolate a bad user token from proxy replacement, destination scope, or propagation problems. A local environment-variable presence is not proof of usable authentication. Defer to the parent's newer authentication evidence if any.
- Saved official ZeroGPU documentation (`../zerogpu_doc_raw.txt`, lines 155–177) gives daily tiers: unauthenticated 2 minutes, free authenticated 5 minutes, PRO/Team 40 minutes, Enterprise 60 minutes. PRO/Team/Enterprise can consume prepaid credits beyond included quota. This review does not authorize subscribing or using paid credits.
- The Space metadata reports `RUNNING`, public/ungated, commit `ebf60b20fc5a4607f90a1c11c0aab0ceeda5429d`, `pySpacesVersion=0.50.2`. Running/public/ungated establishes discoverability and server status, not this account's admission.
- The same session needs two GPU admissions: `/image_to_3d` and `/extract_glb`; source decorators request 120 seconds each (`../space_app_current.txt`, lines 385, 507). Passing generation alone does not prove export can run. Actual quota debit may depend on effective usage/hardware, so multiplying 120 by two is not a verified budget.

## Why 120 versus 176 can occur

The exact publicly reported deployed version, `spaces==0.50.2`, was downloaded from the PyPI distribution URL and checked against the SHA-256 in its version metadata. Both the old before/after-attempt Space metadata and current saved metadata report this version.

1. `spaces_0_50_2_source/spaces/zero/configs.json` defines `duration_factor: 1.5` for NVIDIA RTX PRO 6000 Blackwell Server Edition; the H200 default config uses 1.0.
2. `spaces/zero/client.py:124–135` applies that factor for non-`xlarge` requests before sending `durationSeconds` to the scheduler: 120 × 1.5 = 180 seconds.
3. `spaces/zero/client.py:144–166` builds the rejection message using the original declared duration (only doubling it for `xlarge`), rather than the factored duration. A backend comparison of 180 against 176 can therefore appear as 120 against 176.
4. `spaces/zero/config.py:26–41` selects hardware config by reading the server's NVIDIA driver information. This review cannot read that remote information. Space requirements include Blackwell-related wheel names, and current official docs describe Blackwell hardware, but neither proves which GPU/config was selected for the failed request.
5. `spaces/zero/__init__.py:29–35` can automatically choose `xlarge` if packed memory exceeds the configured threshold. An absent `size=` in the app therefore does not itself prove non-`xlarge`. However this version would display 240 requested for a 120-second `xlarge` function, making the observed 120 more consistent with the non-`xlarge` path.

The multiplier is a stronger concrete hypothesis than an unspecified hidden policy. It does not by itself resolve the earlier `120 vs. 180` rejection, whose equality could depend on backend details/rounding or a separate policy. Backend source and actual hardware/admission telemetry were not obtained. Do not claim every prior rejection has been conclusively explained.

## Anonymous/account policy evidence and limits

- `spaces/zero/client.py:168–173` emits the exact API suffix `Authenticate with a Hugging Face token for more quota` when scheduler metadata `auth` is `None`. This supports the old request being handled as unauthenticated in the matching deployed client version.
- An `X-IP-Token` in that package is the service's routing/admission token, not proof that the caller has a valid Hugging Face account token. The code can also warn that it is falling back to IP-based quotas (`client.py:118–122`). Do not try to manufacture or reuse those internal tokens.
- The displayed 176/180 seconds remaining does not match today's documented 120-second unauthenticated total; the package's PRO suggestion says 25 minutes while current docs say 40. These discrepancies caution against treating documentation or diagnostic strings as live quota guarantees. No specific anonymous multiplier or backend cap was verified.

## What can be verified read-only before generation

- Credential resolution and official `whoami` can verify identity/authentication (parent-owned check).
- GET Space metadata, app source, Gradio `/config`, and published API schema can verify revision, public status, declared endpoints and current runtime availability.
- The saved public API schema exposes start-session, preprocessing, seed/lambda, generation and export endpoints; it exposes no quota/admission preflight endpoint.
- In the exact package, `QuotaInfos(left, wait)` is returned in response to internal `POST /schedule` (`spaces/zero/api.py:88–132`). This operation schedules/reserves GPU work; it is not a read-only quota query, and was not invoked. The internal GET `/queue-size` only measures queue size, is not a published user quota API and cannot guarantee allocation.
- No reviewed official source documents a read-only operation that reserves or guarantees the two required allocations. An account's visible usage/billing information, if the user can inspect it, may inform available budget but cannot guarantee admission. A valid token is a meaningful state change supporting a separately authorized bounded attempt, not proof of execution readiness.

## Source evidence

Existing snapshots: `../zerogpu_doc_raw.txt` with receipt, `../space_app_current.txt` with pinned revision receipt, `../space_meta.json`, `../space_requirements.txt`, `../tokens_doc.txt`, `../../auth_official_client.json`; previous phase `trellis2_car_followup_20261009/FINAL_REPORT.md`, `research/space_live.json`, `research/space_after_attempt.json`, `research/space_api.json`.

New evidence in this directory: `spaces_0_50_2_pypi.json`, versioned wheel with receipt and extracted source, `gradio_python_client.html` with receipt and script-free text extraction, `tokens_doc_text.txt` extracted from the saved token documentation. `evidence_manifest.json` hashes the review's sources and report. No authenticated body, bearer token or internal admission token was saved.

## Follow-up checks requested by parent

Parent reports a new official `HfApi.whoami` check after restart at 10:18 UTC still returned 401. This review did not independently send that authentication request; defer to the parent's saved receipt.

`duration_arithmetic.py` reads only the downloaded hardware JSON and performs arithmetic; it does not import the downloaded package. Its saved result demonstrates Blackwell 120 × 1.5 = 180 and H200 120 × 1.0 = 120. The multiplier explains 176 being below the scheduled amount under the Blackwell/non-xlarge hypothesis; it does not make 180 less than 180.

Local rounding evidence is narrow: schedule duration is explicitly rounded with Python `round()` before POST; `QuotaInfos.left` is typed as `int`, and the error formats `res.left` directly. The remote backend's conversion/rounding of remaining quota and its comparison rule are not in this package. It is therefore possible that backend precision or a separate condition explains the earlier displayed equality, but there is no evidence to select that explanation. Do not call the earlier 120-versus-180 case solved.

Paid overage needs a future budget decision: the current official documentation states that additional usage is automatically billed against prepaid credits after included quota is exhausted for PRO/Team/Enterprise. Valid authentication does not imply a paid-spend authorization. If a future route could draw such credits, establish available included budget or an explicitly authorized spend ceiling before invocation; this review neither purchases credits nor establishes that the account has PRO/credits. Higher-tier auth must not be silently treated as a free execution guarantee.
