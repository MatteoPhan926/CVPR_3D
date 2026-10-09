# Execution notes

- Original downloads copied byte-for-byte and externally checkpointed before processing.
- Native render attempt001 failed because this Blender build lacks OpenImageDenoise. No image rendered. The original script/log are retained. Attempt002 disables denoising; same asset/material/cameras. This is a renderer-build error, not an asset failure.
- User confirmed direct Hugging Face generation and attempted resolutions 512/1536; file mapping, seed, decimation, original-versus-background-removed input remain unknown. Earlier failed-run UI screenshot is excluded as provenance.
- A is selected by filename order for one bounded authoring screen. B is independently inspected but not authored; this limits downstream conclusions to A.
- Native inspection images have a common world-axis camera orbit, not semantic camera matching across A/B (the cars face opposite X directions). No visual ranking or resolution effect is inferred.
