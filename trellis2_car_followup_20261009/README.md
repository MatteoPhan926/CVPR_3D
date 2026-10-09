# TRELLIS.2 car follow-up — 9 October 2026

Current status: official preprocessing succeeded; one hosted TRELLIS.2 generation request was rejected by a ZeroGPU admission error. No new preview, GLB or downstream-use result. See [FINAL_REPORT.md](FINAL_REPORT.md), [SECRETARY_HANDOFF.md](SECRETARY_HANDOFF.md) and [DOWNLOADS.md](DOWNLOADS.md). Initial status is retained in checkpoint 01.
This phase records a blocked attempt at the missing official TRELLIS.2 run using the original grass photograph and original front-door authoring intent. It does not silently replace the model, image, or task. This is separate from the completed TripoSR probe and from an unidentified separately proceeding car experiment. The non-car revision study remains unstarted.

The plan, API metadata, pinned Space source, historical failure and exact input are retained here. `config/generation_plan.json` defines bounded execution and interpretation; `config/INHERITED_AUTHORING_INTENT.md` preserves the original use requirements. One successful candidate maximum; no repeated unchanged quota requests. Historical CPU/TripoSR geometry and vertex-color authoring scripts will not be reused on UV/PBR output without adaptation.

External checkpoints are required before preprocessing, generation, GPU export, and further authoring. Each archive has a complete payload SHA-256 manifest and is downloaded from an immutable GitHub commit into fresh verification storage. Receipts are published separately after read-back. Server-held latent state is not exposed by the public API; this limitation is explicit, not an exclusion of downloadable local latents.

Run the existing remote-client Python with `source/hosted_followup.py` only after satisfying its checkpoint gates. It retains one live Gradio session; API previews and export require that same state. Failed attempts, partial files and logs must be retained. Do not restart the script over attempt001 or rerun inference merely to recover an expired export session.
