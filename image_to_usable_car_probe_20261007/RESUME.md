# Use the completed bounded probe

Work in `/workspace/image_to_usable_car_probe_20261007`. The exact image has arrived, generation and authoring are complete. Read `IMAGE_TO_USABLE_CAR_REPORT.md` first. The result is an informative partial, not an accepted convincing CGI car. Do not repeat generation or select another candidate as part of this completed one-candidate probe. Use the existing checkout; no worktree is needed.

The original image is `inputs/original.jpg`; raw output is `raw/car_raw.glb`; final demonstration is `artifacts/car_authored.glb` and `car_authored.blend`. Both raw and authored bytes are hash-recorded. Historical planning JSON files contain pre-execution zero counts/input-status fields; actual execution is recorded in `raw/*/attempt.json` and the current `config/attempt-log.json`. The failed hosted route produced no candidate. CPU produced exactly one.

Run the offline viewer from the probe root:

```bash
python3 source/viewer/serve.py --bind 127.0.0.1 --port 8777
```

Processes do not survive environment restoration. Keep this server running while using the viewer. Its root redirects to `/source/viewer/`. If the port is occupied by an unrelated process, choose a different port and adjust checks. Do not offer loopback preview links in the onboarding UI. See `source/viewer/README.md` for tested browser verification and rebuild commands. The bundled `dist/app.js` runs offline without npm installation.

The CPU venv, exact official checkpoint and preprocessing caches are retained under `environment`; no GPU or credential is needed to inspect or author the saved assets. The compact evidence ZIP excludes these large replaceable dependencies, duplicate raw exports, cached neural codes, cut intermediates and redundant render sets. Full diagnostics remain in the workspace; the archive includes the unchanged canonical raw GLB, both authored GLBs, editable final Blender file, selected before/after/exposed-surface images and verification records. Refresh dependencies only when needed using `bash source/setup_cpu.sh` and `environment/venv/bin/python source/acquire_models.py`. Never overwrite the recorded attempt outputs by rerunning generation. The setup uses verified downloads and pinned source revisions.

To reproduce the final conventional authoring from retained raw bytes (this overwrites generated authoring outputs; preserve local edits first):

```bash
environment/venv/bin/python source/cut_door.py
blender -b -t 4 --python-exit-code 1 --python source/author_car.py
blender -b -t 4 --python-exit-code 1 --python source/verify_authored.py
```

These scripts are the executed authoring/reopening path. The GLB includes a four-second open/close clip; the viewer maps the opening interval at 1/30–61/30 seconds to 0–60 degrees. Expected body transform deltas are zero, and sampled angle tolerance is 0.01°. These checks do not establish appearance acceptance or physical clearance. Proxy completion is disclosed, not recovered ground truth.
