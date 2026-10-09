# Verified downloads

[Compact research report, secretary handoff and selected evidence ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/c344c863aab527bececa307b29547e96597a0725/research_decision_delivery_20261009/RESEARCH_DECISION_OUTPUT_20261009.zip) — 4,351,865 bytes.

Compact ZIP SHA-256: `764eec7ccd424fbe7c6f731e5236f65e5362cd85ebac142145cd9d6f3ab44933`.

The compact ZIP is an immutable snapshot at data commit `c344c863aab527bececa307b29547e96597a0725`; later publication metadata/receipts are outside that ZIP. It contains 52 payload files plus its manifest. No large mesh/latent/array evidence is silently substituted or deleted; those files are in the full recovery archives below.

| Full archive | Bytes | Immutable download |
|---|---:|---|
| 01_research_generation.zip | 76762708 | [Download](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/01_research_generation.zip) |
| 02_research_controls_and_holdouts.zip | 55555761 | [Download](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/02_research_controls_and_holdouts.zip) |
| 03_car_probe.zip | 77998874 | [Download](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/03_car_probe.zip) |
| 04_dependency_source_and_metadata.zip | 34785124 | [Download](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/04_dependency_source_and_metadata.zip) |
| 05_bentley.zip | 58048846 | [Download](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/42dc0ea31f75e8783bf1f208b8fb83d523ab076c/recovery_checkpoint_20261008/archives/05_bentley.zip) |

All five full archives were previously downloaded and verified: 813 payload files, including all three latents. Checksums and exact coverage are in [FULL_EVIDENCE.json](FULL_EVIDENCE.json).

[Current delivery receipt](DELIVERY_VERIFICATION.json) · [Full recovery receipt](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/8df00f1481b2e75741eb01e6c076315f9d60f6bb/recovery_checkpoint_20261008/EXTERNAL_VERIFICATION.json)

To restore full evidence with Python 3.11+ standard library into a new directory:

```bash
python3 download_full_evidence.py --commit 42dc0ea31f75e8783bf1f208b8fb83d523ab076c --destination ./recovered-evidence-new
```

Do not extract over an existing workspace. Installed environments and upstream weights are explicitly excluded from the full portable backup.
