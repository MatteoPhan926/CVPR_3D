# Narrow CPU route review: official TripoSR

**Recommendation:** TripoSR is a justified CPU-capable alternative for a bounded single-image-to-colored-GLB attempt. The current concrete blocker is acquiring its pretrained artifacts from Hugging Face through the configured network. Dependency preparation may proceed independently, but installing packages cannot resolve model acquisition. No inference or export was executed in this review; therefore these findings do not establish car quality, CPU runtime, peak memory, or a usable asset.

## Primary-source findings

- Official `run.py` explicitly falls back to `cpu` when CUDA is unavailable, accepts `--device cpu`, and moves the model and input to that device. Its timer only calls CUDA synchronization when CUDA is available. `tsr/system.py` loads checkpoint tensors onto CPU. This is an implemented CPU path, not merely an assumption from a generic PyTorch API.
- `torchmcubes` is not an unavoidable CUDA blocker. Its upstream `CMakeLists.txt` checks for a CUDA compiler and otherwise builds a CPU version. `torchmcubes/__init__.py` directly calls `mcubes_cpu` for CPU tensors. Current upstream documents C++20, CMake >=3.18, and a build against already installed PyTorch with `--no-build-isolation` plus scikit-build-core and pybind11. The TripoSR requirements use an unpinned Git dependency; the resolved immutable revision is recorded below.
- Ordinary colored GLB is an official CLI path: `--model-save-format glb`, leaving `--bake-texture` absent. `extract_mesh(..., has_vertex_color=True)` queries the neural color field, constructs a trimesh mesh with vertex colors, and `meshes[0].export(...)` serializes it. This does not guarantee faithful thin details, transparency, door seams, disconnected parts, or an interior.
- Avoid optional texture baking for this CPU/headless probe. `bake_texture.py` requires `moderngl.create_context(standalone=True)` and OpenGL GLSL 330 to rasterize the atlas; it separately exports an image and uses `xatlas.export`. That is extra context/export integration to validate and is unnecessary for vertex-colored GLB. The modules are imported unconditionally by `run.py`, so their Python packages remain required even when their GL context is never created.
- Hugging Face artifacts required by the actual implementation are `stabilityai/TripoSR/config.yaml`, `stabilityai/TripoSR/model.ckpt`, and `facebook/dino-vitb16/config.json`. The last fetch is in `DINOSingleImageTokenizer.configure()` even when the main model comes from a local directory. A complete preexisting authenticated/cache binding could satisfy these; a local checkpoint alone does not establish readiness. This review did not request secrets or bypass the proxy.
- The official preprocessing path uses `rembg.new_session()`, removes background, fits foreground at ratio 0.85, and composites on gray. It saves processed `input.png`. Its first run may require rembg model acquisition in addition to TripoSR. Preserve the original attachment and that processed input. Do not silently run the scene photograph with `--no-remove-bg`; that option expects an already prepared gray-background image.
- `TriplaneNeRFRenderer.query_triplane()` uses chunked standard PyTorch grid sampling and MLP evaluation. `--chunk-size` limits query batches but does not eliminate the full marching-cubes grid allocation. At default resolution 256, the float32 XYZ grid alone is about 192 MiB. The official README's ~6 GB VRAM claim concerns its GPU default and is not a measured CPU RAM guarantee. Linux with five CPUs and ~32 GiB RAM is plausible for this route; no CPU timing/memory measurement was made here.

## Bounded configuration if acquisition becomes available

Retain default extraction resolution 256 and foreground ratio 0.85; explicitly select CPU, use chunk size 4096, vertex-color GLB, and no optional NeRF video or texture bake. Cap CPU threads to five, record the complete installed dependency versions and upstream revisions, and impose a documented inference time budget rather than speculative repeated repairs. Example command (not executed):

```sh
OMP_NUM_THREADS=5 MKL_NUM_THREADS=5 python run.py ORIGINAL_INPUT --device cpu --pretrained-model-name-or-path MODEL_DIR --chunk-size 4096 --mc-resolution 256 --foreground-ratio 0.85 --model-save-format glb --output-dir RAW_OUTPUT_DIR
```

`MODEL_DIR` must contain the authorized downloaded upstream configuration/checkpoint, and the DINO configuration plus rembg artifact must also be available. These placeholders are intentional; there are no such verified artifacts in this review.

## Evidence and scope

Saved unmodified primary source snapshots and SHA-256 hashes are listed in `fetch-manifest.json`. Every successful TripoSR/torchmcubes branch-source fetch was fetched again using the immutable commit below and matched byte-for-byte. Package publisher metadata and the official CPU wheel index are separate primary-source snapshots. Workspace resource evidence and the Hugging Face CONNECT 403 were inspected in the parent task's `../resources.json` and `../access-checks.json`. That recorded 403 is a transport/acquisition limitation; it says nothing about reconstruction quality. This review fetched only official public source over the existing configured network. It did not install dependencies, fetch weights, mutate source, generate a mesh, or render an asset.

## Reproducible source and proposed Python 3.12 stack

Resolved using read-only `git ls-remote` on the upstream repositories, then verified by fetching each saved source at that immutable revision:

- TripoSR: `107cefdc244c39106fa830359024f6a2f1c78871`.
- torchmcubes: `879926d0ef58e6ce0ac2630fdecb5e53af7ed3ff`.

The unchanged `requirements.txt` in this folder is the exact TripoSR dependency declaration. Its exact pins are `omegaconf==2.3.0`, `Pillow==10.1.0`, `einops==0.7.0`, `transformers==4.35.0`, `trimesh==4.0.5`, `xatlas==0.0.9`, and `moderngl==5.10.0`; rembg, huggingface-hub, imageio[ffmpeg], gradio and Git torchmcubes are unpinned. PyTorch is documented as a prerequisite but has no version pin. The current torchmcubes pyproject requires `scikit-build-core>=1.0` and `pybind11>=2.10`; its CPU CI matrix includes Python 3.12. This is source-level declared CI coverage, not a claim that this workspace passed that CI.

**Proposed candidate, not an upstream tested lockfile:** Python 3.12 with `torch==2.5.1+cpu`, `numpy==1.26.4`, `rembg==2.0.59`, `onnxruntime==1.20.1`, `opencv-python-headless==4.10.0.84`, `tokenizers==0.14.1`, `huggingface-hub==0.17.3`, and the exact upstream pins above. If installing the full optional UI dependency declaration, constrain `gradio==3.50.2`; the CLI itself does not import gradio. These choices must pass the real resolver, `pip check`, import tests and the marching-cubes CPU smoke test before they count as a working stack.

Why these specific candidate constraints:

- The official PyTorch CPU index was accessible and explicitly lists `torch-2.5.1+cpu-cp312-cp312-linux_x86_64.whl`, SHA-256 `4856f9d6925121d13c2df07aa7580b767f449dfe71ae5acde9c27535d5da4840`. Install via the official CPU index rather than generic PyPI torch, whose Linux 2.5.1 metadata includes CUDA dependencies. Only the index was read; the wheel was not downloaded here.
- NumPy 1.26.4 has a CPython 3.12 Linux wheel. This is a conservative constraint for TripoSR's 2023-era trimesh/transformer pins, not a claim that NumPy 2 is unsupported by every component.
- rembg 2.0.59 declares Python `>=3.8,<3.13` and the ordinary CPU `onnxruntime` dependency. The chosen ONNX runtime has a CPython 3.12 Linux wheel.
- OpenCV headless 4.10.0.84 declares NumPy >=1.26.0 for Python 3.12 and provides a compatible abi3 Linux wheel, so it avoids unconstrained future OpenCV releases forcing NumPy 2.
- transformers 4.35.0 requires tokenizers >=0.14,<0.15. tokenizers 0.14.1 supports Python 3.12 by wheel but requires huggingface-hub >=0.16.4,<0.18. The proposed hub 0.17.3 satisfies both; current unconstrained Gradio may not. Gradio 3.50.2's metadata permits that hub version, NumPy 1.26 and the pinned Pillow 10.1.0.
- xatlas 0.0.9 explicitly has a CPython 3.12 Linux x86_64 wheel, so its age alone is not a Python 3.12 blocker.

Metadata evidence is in `version-evidence.json` and its fetched publisher files; official CPU wheel evidence is in `cpu-wheel-evidence.json`. This is a candidate compatibility argument, not a full dependency resolution or executed inference claim. No package installation was performed by this review.
