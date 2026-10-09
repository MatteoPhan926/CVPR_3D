# Independent history and opportunity assessment

8 October 2026. Scope: broad objective **2D input → generated 3D asset → meaningful artist/downstream use**. This review read the supplied historical discovery/reproduction/authoring records before receiving other investigators' new findings. It did not read the new external audit. No downloads, model inference, asset generation, rendering, changes to historical workspaces, or artist trials were performed here.

**Recommendation:** authorize at most a small export-interpretation holdout screen, then decide whether to keep an engineering correction, pursue a specific residual, or stop. The old negative allocation does not rule out useful generated assets; the available evidence also does not establish a publishable unsolved mechanism. Do not commission another general articulation/topology campaign from these records.

## What is actually available

Fresh inventory: [artifact_inventory.json](artifact_inventory.json). It traversed the three assigned historical workspaces, skipping dependencies/caches where appropriate, inspected both retained delivery ZIPs, parsed GLB metadata, computed hashes, and read local Git metadata. It did not query the remote server.

| Evidence | Available here | Limit |
|---|---|---|
| Bentley authoring | Input and authored GLBs, scripts/configuration, original reports, validation records, images and source bundle | The input is a supplied GLB. Exporter metadata is Blender glTF I/O, not proof of image-conditioned generation. No source 2D input or generation chain is retained. |
| Citroën/TripoSR probe | Source photograph, preprocessing, saved latent, one raw candidate, two authored versions, scripts, viewer, .blend scenes, logs | One image-conditioned successful generation. Its strict convincing-CGI target failed; no human artist utility measurement. |
| Particulate folding chair | Detailed report and complete compatibility patch | The actual foldingchair.glb, eight output files, checkpoints, prediction arrays and validators described in the report are absent from the inspected roots/archives. Cannot replay quality or trajectories here. |
| Older support/kinematics and pivot studies | Summary values and interpretation in discovery decision | Coordinate data, old meshes, inference module and complete experiment archives are unavailable in these roots. Their conclusions remain historical reported evidence. |
| Non-car local candidates | Fourteen official TripoSR example images, including teapot, hamburger, chair and house, plus installed source/checkpoints | These are 2D inputs. No corresponding non-car generated GLB/OBJ/NPZ was found in the assigned historical workspaces. A new generation would be new evidence, not a replay. |

There are **five unique GLB hashes** across nine loose GLB paths: Bentley original/authored and TripoSR raw/v1/final. Several copies are delivery duplicates, not additional experimental cases. Other Blender/NPZ assets are states of those same cars. Bentley ZIP: 74 entries, only its two car GLBs plus source bundle. Car ZIP: 170 entries, only raw/v1/final car GLBs and final .blend.

The local CVPR_3D repository was clean, with 178 tracked files and two reachable commits: `a04ddf538c72a3b34904845474395feccc31458a` (Bentley package) and `6b99f54997c17e5d1f26bab89e1b2ecdaab2f838` (image-to-car package). Local branches were `work` and `image-to-usable-car-20261007`, with cached `origin/bentley-download-20261006`. This says what is present locally; it cannot prove no other remote or external experiment exists. Separately active car/non-car revision work is outside this inventory and must not be duplicated.

## New measurements executed here

[audit_glb_contract.py](audit_glb_contract.py) reads the four final input/output GLBs directly, decodes accessors and scene transforms, hashes embedded images, compares unchanged accessor values, and measures world-space rest surface areas. Its independent result is [artifact_contract_measurements.json](artifact_contract_measurements.json). Run with `PYTHONDONTWRITEBYTECODE=1 python audit_glb_contract.py`.

| Measurement | Fresh result | Interpretation |
|---|---:|---|
| Bentley image payloads | All 24 hashes identical | The appearance data survives the edit. |
| Bentley material and texture definitions | Identical | No texture regeneration or material replacement was necessary for supplied rigid editing. |
| Bentley untouched geometry | All attributes/indices identical on eight original meshes | Local authoring can preserve unaffected data exactly. |
| Bentley total rest surface area change | −1.72×10⁻¹⁰ model units² | Numerically conserved; not a proof of semantic boundaries or collision freedom. |
| TripoSR moving exterior area / raw area | 6.8722% | Most generated outer surface remains fixed; failure is not automatically caused by a global topology edit. |
| TripoSR authored exterior area relative change | −9.05×10⁻¹⁰ | The retained exterior is an area-conserving partition. |
| TripoSR added lining/jamb/cabin area / raw area | 28.0587% | The final appearance includes appreciable authored completion, so raw vs final is not an isolated test of door motion. |
| TripoSR added triangles / raw triangles | 10.7343% | A surface-count descriptor, not an estimate of human effort. |
| TripoSR exterior partition triangle increase | 5,904 | Clipping changes triangulation despite conserving area. |

The raw TripoSR GLB has COLOR_0 but no NORMAL and no explicit material. The authored exterior adds normals/materials; added proxies add further geometry/materials. Fresh parsing confirms those attribute differences. Area conservation alone cannot establish unchanged shape at every point, correct door ownership, compatible shading, or downstream usability. No new collision, image similarity or animation playback test was executed here.

## Overlooked successes and confounded failures

1. **The Bentley is a real successful supplied-asset authoring example, with a missing upstream provenance link.** The historical report says its motion was reopened in Blender/Chromium, rest appearance essentially preserved, textures kept, and output regenerated byte-identically. The new binary checks support the preservation portion. This undercuts “generated triangle meshes inherently cannot support useful rigid authoring,” but cannot be counted as demonstrated image-to-usable-asset generation because its image-generation provenance is missing. User acceptance and saved labor remain unmeasured.

2. **The Particulate memory failure was repaired and should stay repaired in the research memory.** The historical report records decoder chunking after full attention: 4,097-point equivalence probe passed with max absolute error 2.26×10⁻⁶ and zero label disagreements, then 102,400-point full inference/export succeeded. This is historical execution evidence, not a fresh replication. Original OOM and a 600k-point terminated run cannot support model-quality negatives. Conversely, two structurally valid predicted chair parts do not establish a correct fold. Ignored GLB node rotation, multiple coordinate normalizations and strict connected-component labeling are concrete interpretation issues that should be checked before diagnosing representation failure.

3. **The TripoSR car establishes the chain only through controllable output, not compelling appearance.** One candidate was produced in about 42.5 seconds and made controllable. TRELLIS.2 returned no candidate because of service quota, so it has no quality result. The TripoSR result entangles source-image fidelity, novel-view reconstruction, mesh extraction, exported color/material interpretation, normals, selected door contour and newly exposed interior completion. The original report already discloses raw/default metallic shading and authored smooth normals. It is reasonable to retain obvious shape deficits, but not attribute every visible discrepancy to generator failure.

4. **The historical research rejection was formulation-specific.** The tested conditional pivot estimator's approximately 0.0294% mean improvement is a narrow negative result. The appearance/contact/hidden-state directions were mostly rejected formulations, not empirical falsifications. The 1.25% versus 9.89% oracle advantage under different endpoints is a warning about measurement alignment: matched-set geometry can hide material-point ownership error. None of these facts supplies a new method merely by changing labels.

5. **Meaningful downstream use was repeatedly replaced with stronger or different requirements.** Convincing close-up car CGI, mechanism accuracy, collision freedom, material relightability and artist time savings are distinct tasks. A controlled static prop or camera-path preview can be useful without satisfying all of them, but “it loads and rotates” does not establish that usefulness either. The next measurement should choose one actual use and a competent alternative before observing the result.

## Two bounded measurements with the most decision value

These are proposed follow-ups, not completed results. The first was refined after root reported independent color/export findings; those findings are not claimed as this agent's executed evidence. Neither task duplicates non-car revision/editing work.

### 1. Export interpretation on two non-car holdouts

**Decision:** is apparent failure sufficiently explained by conventional display/export choices that the practical next step is a compatibility fix, or does a task-relevant residual remain?

Use the official teapot and hamburger example images as small export-only holdouts if the root's experiment scope permits their one-time generation. Keep geometry/vertex positions, camera, framing, background, exposure, tone mapping and culling fixed. Save the same candidate in three conventional forms:

- Original exporter output.
- Explicit appearance-preserving unlit glTF, with the encoded/linear transfer conversion justified by the producer's display path.
- Explicit dielectric lit material plus a disclosed standard normal policy and the same conversion.

First reproduce each material's intended interpretation on a simple color fixture; do not choose conversion per asset. Measure masked pixel errors against a same-mesh reference renderer to isolate file/renderer interpretation. Separately compare against native-field images when available, retaining silhouette/coverage error as an extraction residual rather than calling it an export error. Region summaries should distinguish interior pixels and silhouettes; no per-image exposure fitting. Hash geometry and raw appearance samples to prove no asset improvement was smuggled into the conversion.

**Why this is feasible:** the raw GLB contract problem can be isolated without editing the asset, changing topology, obtaining new mechanical labels, or doing a full artist study. Most required source and rendering infrastructure already exists. Root's separate field→mesh investigation should supply that part; do not duplicate it.

**Strongest alternative explanation:** these are ordinary color-space, material and shading conventions. Official TripoSR `system.py:144` writes renderer RGB directly to 8-bit PIL, while `system.py:194` samples the same field for vertex color. That supports a display-compatibility investigation, not proof that the values are physical reflectance. The renderer has no independent lighting input. Unlit matching appearance but ignoring light is expected; it is not a new trade-off discovery.

**Stop/reframe rule:** if a standard conversion removes the discrepancy, retain the engineering fix and close the export-as-research route. If native field and conventionally exported mesh both fail the task, stop blaming format interpretation and classify the remaining source-fidelity/extraction limitation. If the discrepancy survives on both held-out objects, inspect its cause before any new mechanism claim. Two official examples establish reproducibility at most, not population prevalence or novelty.

### 2. A downstream preview task against an image-plane baseline

**Decision:** after conventional export correction, does this 3D candidate provide useful capability beyond displaying the source picture?

Predeclare a modest concrete task: place the asset in a simple scene and deliver a fixed short camera path, with the intended screen size and angular excursion set before review. Compare the corrected GLB with a competent source-image billboard/alpha-card baseline using the same camera path and placement. Retain a native-field preview if available as the attainable higher-fidelity non-editable alternative. Do not add articulation, invisible interiors or arbitrary relighting requirements to this task.

Measure preparation time, bounded correction actions, artifacts along the camera path, and acceptance of the rendered clip for that specific use. An actual artist can provide the utility judgment; absent one, label assistant scoring a technical screen and leave user acceptance unassessed. A technically successful GLB export is not an artist study. This small task can distinguish useful parallax/occlusion/placement from a showcase that could be satisfied by a static image.

**Stop/reframe rule:** if an image plane suffices, the task does not justify a generated 3D method. If the corrected GLB is useful with no new algorithm, retain the workflow as an application result. If standard output fails because a demanded close view or light change reveals baked illumination/shape error, that is a sharply identified missing capability, but an appropriate intrinsic-material or geometry baseline is needed before a research allocation. No new literature survey is needed to discover that unlit materials are not physically relightable.

## What would not justify a new project

- Unlit rendering beats lit rendering at preserving baked appearance, or lit rendering responds more to lights: built into the definitions.
- A color transfer adjustment improves screenshots: expected conventional calibration unless a more consequential unsolved constraint is demonstrated.
- A collision/door boundary score worsens after showing previously hidden interiors: a changed task, not evidence that all retained surface topology is inadequate.
- A neat viewer or zero validator errors: useful delivery infrastructure, insufficient evidence of artist benefit.
- A missing old artifact: a current reproducibility limit, not evidence that the scientific direction is impossible.

The strongest present course is **bounded practical measurement with a stop rule**, not commitment to a new representation paper. The available successes already support an appearance-preserving authoring baseline; any new method must demonstrate a consequential benefit beyond that and beyond ordinary display/material conventions.
