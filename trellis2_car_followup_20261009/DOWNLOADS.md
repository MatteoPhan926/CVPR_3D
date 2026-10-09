# Downloads and external checkpoints

Repository branch: [trellis2-car-followup-20261009](https://github.com/MatteoPhan926/CVPR_3D/tree/trellis2-car-followup-20261009/trellis2_car_followup_20261009).

For the complete handoff, use `checkpoints/05_final_delivery.zip` and its adjacent manifest and verification receipt. The receipt names its immutable data commit and download URL; a ZIP does not contain its own later verification receipt. All earlier archives and receipts remain separately retained in Git. Download verification means a fresh external HTTPS download, whole-archive hash, every member hash, safe extraction into a new directory and reread.

| Checkpoint | Immutable data commit | Download | Read-back |
|---|---|---|---|
| Initial input/contract/source (19 files) | `5865ece4300fd4d06f009e6a8daa85a6cd03bb13` | [01_initial.zip](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/5865ece4300fd4d06f009e6a8daa85a6cd03bb13/trellis2_car_followup_20261009/checkpoints/01_initial.zip) | Verified |
| Corrected client and original import failure (22 files) | `59fadb69b2cf13802d018e4109a3eeeb21532a11` | [02_client_correction.zip](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/59fadb69b2cf13802d018e4109a3eeeb21532a11/trellis2_car_followup_20261009/checkpoints/02_client_correction.zip) | Verified |
| Preprocessing before generation (29 files) | `5f0c51b9dbb884e9ca1e3504ef00c459965c1b39` | [03_preprocessing.zip](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/5f0c51b9dbb884e9ca1e3504ef00c459965c1b39/trellis2_car_followup_20261009/checkpoints/03_preprocessing.zip) | Verified |
| Exact service rejection, all returned output (32 files) | `99f39acd85b975eca3ec71dc879b4d398c55821c` | [04_admission_blocked.zip](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/99f39acd85b975eca3ec71dc879b4d398c55821c/trellis2_car_followup_20261009/checkpoints/04_admission_blocked.zip) | Verified; [receipt](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/02b31af4a0d07235684c180642c1ca5ff38a7ff1/trellis2_car_followup_20261009/checkpoints/04_admission_blocked.verification.json) |

Exclusions: externally retained earlier checkpoint archives are not recursively included in later ZIPs. Installed dependencies, replaceable model weights, credentials, VM state and live sessions are not copied. No new local mesh or latent was generated/returned and omitted. Server-held latent state is not exposed by the hosted API and cannot be claimed protected. Prior research, meshes, arrays and three latents remain in the separate verified 813-file recovery package linked from [SECRETARY_HANDOFF.md](SECRETARY_HANDOFF.md).
