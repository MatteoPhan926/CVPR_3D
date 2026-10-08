# Research artifact recovery — 9 October 2026 (Asia/Bangkok)

This checkpoint preserves actual files recovered from the original cloud workspace. No setup, build, render, inference, numerical refinement or research experiment was rerun during recovery. Source working directories remain unchanged.

## What was recovered

- All 401 files found under `/workspace/research_decision_20261008` at snapshot time, including unfinished outputs, failed logs, source, arrays and figures. The per-file manifests are authoritative if a narrative count differs.
- The original car latent plus the teapot and hamburger latents. All are research artifacts, not discarded caches.
- Both saved density grids, intermediate meshes, mesh arrays found under the old probe's environment directory, Blender files including earlier versions, photographs, preprocessing records and logs.
- Original audit/task attachments; Bentley/probe evidence and source; actual TripoSR/torchmcubes source; installed package version inventory; non-secret onboarding configuration.
- 808 source files in total, plus 5 recovery metadata files: 813 payload files. Each copied source file matched its source hash during preservation; no copy errors were recorded.

## Existing results, inspected rather than rerun

| Work | Evidence/status |
|---|---|
| Generator provenance and field/mesh controls | Preserved under [generation_execution](evidence/generation_execution/). The audited car used TripoSR CPU; hosted TRELLIS.2 produced no candidate. Decoder replay and re-extraction records remain available. |
| Authoring attribution | [Measurements](evidence/authoring_attribution/measurements/): matched display controls, partition effects and selection components. Material/display settings materially confound old visual comparisons. |
| Historical artifact checks | [History report](evidence/history_opportunities/HISTORY_OPPORTUNITIES.md): preserved Bentley texture/geometry contracts; historical execution success separated from quality claims. |
| Two non-car generation controls | [Teapot](evidence/root_analysis/holdouts/teapot/execution.json), [hamburger](evidence/root_analysis/holdouts/hamburger/execution.json). Raw meshes and saved latents are in ZIP 02. These are static export/extraction controls, not an artist revision trial. |
| Edge refinement | [Aggregate](evidence/extraction_control/verification_and_aggregate.json): improved agreement with the model's native field across the three explored objects. This is not ground-truth object accuracy or artist usefulness. |
| Saved forward replay, previously unconfirmed | Recovered [JSON](evidence/root_analysis/saved_forward_reproduction.json) records one replay, exact tensor equality and maximum absolute error 0.0. This is an existing completed result, not a new recovery-time run. |
| Browser export validation | Recovered [log](evidence/root_analysis/browser/verification.log) ends in a timeout waiting for `window.testAPI`; no pass is claimed. The earlier missing-SciPy log is also retained. |
| Log-density comparator | Recovered [log](evidence/extraction_control/log_density_run.log) ends in an assertion on `renderer.cfg.density_activation`. No completed comparator result is claimed; no repair was attempted during recovery. |
| Adversarial review | [Draft review](evidence/adversarial_review/REVIEW.md) and source receipts retained. Direct prior exists for edge bisection; the draft is not final approval. |

The strongest unresolved interpretation remains improved numerical/display agreement with the model itself, rather than improved artist utility. No CVPR/ICCV contribution is established by recovery. Research continuation is paused until preservation is verified and the user authorizes the next phase.

The separately mentioned car experiment still has unknown run metadata. No generator or contract is assigned to it. The proposed non-car revision study is not treated as a confirmed run.

## Coverage limits

[Source manifest](source_manifest.json) lists every included source file, hashes, stability checks and exclusions. Only explicit installed environments, dependency caches, model download caches, dependency Git metadata and rebuildable extension outputs are excluded. Actual dependency source, environment mesh arrays, latents and experimental results are included. No original cache or weight was deleted.

The checkpoint does not preserve the VM itself, running processes, credentials, installed binary environments or downloaded upstream weights. Those are separate from the experimental artifact coverage. Exact acquisition receipts, pinned model/source identity and installed versions are retained.

[MANIFEST_SHA256.json](MANIFEST_SHA256.json) covers every payload file. [CHECKPOINT.json](CHECKPOINT.json) lists the five independently readable ZIP archives. Each archive is below 90 MiB and carries its own subset manifest. The original local monolithic ZIP and split chunks are staging products, not the public delivery format.

## Verification

The initial data commit records packaging as awaiting external verification. A later `EXTERNAL_VERIFICATION.json` records the exact data commit, immutable download URLs, all archive hashes, all extracted file checks and latent hashes. Treat the verification receipt as the completion record; an upload alone is insufficient.

