# Independent brief review: available outputs to meaningful artist use

Date: 2026-10-09. This review inspected the brief, historical reports/handoffs, source scripts and the JSON chunks of both newly supplied GLBs. It did **not** render, alter, import or author either supplied asset. Earlier reviewers' visual conclusions below are attributed historical evidence, not a fresh independent visual judgment. A later parent-requested inspection of the parent's saved A renders and original reference is recorded separately in `HINGE_REGION_REVIEW.md`; it does not retroactively turn the historical review into a new rendering experiment.

## Finding

The current evidence supports running a bounded, competent conventional downstream screen. It does not select topology, segmentation, geometry extraction or joint prediction as the contribution. The inherited car task is demanding enough to expose useful failure modes, but ordinary tools are explicitly allowed to solve it. A successful conventional result would be useful engineering evidence; a failure of one recipe would not establish that generated assets generally cannot support artist use.

The broad objective is 2D input → generated 3D → meaningful artist use. This car's opening door is a concrete instance, not a definition of all useful 3D. A car that serves scene placement or camera blocking yet fails a close-up door shot has limited, task-dependent utility. Such a partial result must not silently replace the declared door target or become a claim that all artist use failed.

## What is actually required

| Requirement | Evidence and interpretation |
|---|---|
| Preserve this recognizable vehicle | Inherited intent lines 3 and 7 names the supplied grass photograph and appearance cues: dark body, upright cabin, tall narrow chevron grille, round lamps, separate fenders, bright bumper and relative silhouette. It does not demand exact unseen geometry. |
| Move the intended front cabin door | Intent line 5 locates the camera-facing front door behind the windshield and ahead of the rear door. Glass, frame, handle and lining must move coherently, with other vehicle parts fixed. A rotating arbitrary exterior patch is insufficient. |
| Continuous, reversible 0–60° | Intent line 5 requires a slider and short open/close demonstration. The follow-up FINAL_REPORT.md clarifies two seconds opening plus two seconds closing, matching the historical 121-frame/30 fps script. Record timing explicitly, since the older intent's wording alone is ambiguous. |
| Convincing visible opening | Intent lines 7–9 requires whole-car hero and nearby side views around 1440×960, saved 0/30/60° states, and an oblique door-edge/cabin close-up. There must be an aperture, plausible thickness and interior, with no conspicuous tearing or gross visible intersection. |
| Conventional preparation is allowed | Intent line 9 explicitly permits selection, cuts, local remeshing, lining/jamb completion, material repair and pivot authoring. No automatic-semantic-part or pristine-topology requirement exists. |
| Honest boundaries | Plausible unseen completion is acceptable; physical scale, collision certification and unseen-surface accuracy are not presumed. Intervention/material changes and failed attempts must be retained. Runtime is not human labor. |

Original task lines 18–25 also require choosing methods without presuming topology/segmentation/joints explain failure, and permit an informative partial result or evidenced blocker. No numeric human-labor budget or fixed general-purpose quality threshold was established in that brief.

The original one-successful-inference restriction describes the historical acquisition probe. Two newly supplied outputs now exist; that must be disclosed rather than pretending the current phase is still a single precommitted inference. No further generation is required. Retain and report A and B, and avoid selecting the more attractive one and presenting it as the only result.

## Direct metadata observations on the supplied assets

Read-only JSON inspection of both files found:

- One mesh primitive with POSITION, TEXCOORD_0 and NORMAL attributes; no COLOR_0 attribute.
- Embedded WebP base-color and metallic/roughness textures; EXT_texture_webp; one opaque, single-sided PBR material; no animations.
- Base-color factor [1,1,1,1], metallic factor 1 and roughness factor 1. **Those factors multiply texture channels; they do not mean the entire textured asset has uniform metallic=1 and roughness=1.**
- `asset.generator` is `https://github.com/mikedh/trimesh`, which identifies an exporter, not the upstream model or generation settings.
- No top-level extras or explicit generation settings were found in the inspected JSON. File size/timestamp cannot identify resolution or seed.

These are format observations only. A single primitive does not mean one connected component or one semantic part. Opaque material does not by itself establish that the door task fails. The images can contain a plausible opaque glass appearance. Native imports, display fidelity, geometry quality and door suitability remain unassessed by this reviewer.

Authoritative current provenance is `../../inputs/PROVENANCE.json`: user-reported TRELLIS.2 after Hugging Face sign-in; unknown per-file resolution, seed, export settings and independently verified exact input linkage. A and B are filename-order labels, **not** a controlled resolution comparison.

## Historical findings and confounds

1. **Generator identity and resource failure.** The actual completed historical car was one TripoSR CPU candidate, not TRELLIS.2. The later TRELLIS.2 follow-up returned no preview/GLB; the route-resolution phase only inspected a separate public sample. Their service failures and public-sample format defects cannot be assigned to the user's two new assets. Historical FINAL_REPORT.md files state this directly.

2. **Display/material confound.** The old car report lines 21–23 and `logs/authoring-revisions.md` document different raw Blender/browser material and normal treatments. `author_car.py` lines 11–22 builds a new vertex-color material, then sets metallic=roughness=1; lines 27–33 creates geometry from arrays and smooths polygons. Historical research synthesis reports substantial appearance changes from a material-only intervention. Thus an old appearance difference is not automatically a generation defect.

3. **The old cutter is not a UV/PBR-preserving baseline.** `cut_door.py` lines 13–20 concatenates the scene, transforms positions and reads vertex colors. Its Builder, lines 50–65, carries only positions and colors; line 90 saves only geometry/colors/boundary. `author_car.py` reconstructs the meshes. UVs, original materials/textures, tangent/normal handling, material assignments and node hierarchy are not carried through that pipeline. Running it unchanged on A/B would discard precisely the representations now present. A custom cutter must carry per-corner UVs and material assignments across cuts and respect seams; ordinary Blender editing that preserves them is an equally valid baseline.

4. **Selection/completion competence was not established.** The old cutter uses a fixed convex projected outline plus an X threshold (lines 21–36), specific to the old car. It does not discover a semantic boundary. Historical research synthesis line 18 reports a detached predominantly horizontal component comprising 14.39% of selected area. That is evidence for an alternative selection explanation, not a clean test of topology. Reusing old coordinates is expressly disallowed.

5. **Crude interior completion was a real intervention.** `author_car.py` lines 41–57 offsets an entire selected skin along X, creates edge/jamb strips, and adds four cabin boxes at fixed coordinates. This can create a moving shell and still fail believable glass/lining/cabin requirements. The report records one correction for boxes protruding through the silhouette. Such a recipe is not the ceiling of ordinary DCC authoring; failure does not prove inaccessible semantics or missing topology is the necessary cause.

6. **Mechanical success and visual success differ.** The old report lines 19 and 29 reports area partition, static transforms, exact close return, slider behavior and zero glTF errors, while lines 3 and 21 reports the convincing-CGI target failed. Area preservation says nothing about correct moving part or visual clearance. Conversely, validator defects need not explain a visible task failure if the target DCC displays/edits adequately.

7. **Extraction diagnostics answer another question.** The research decision's native-field rendering agreement and edge bisection results measure internal representation consistency. It reports conventional prior and strong refreshed-color effects. These do not measure fidelity to this photograph, user acceptance, task completion or labor saving, and they do not select an intervention for the newly supplied files.

8. **Other historical assets are not equivalent experimental samples.** Bentley supported ordinary authoring but lacks confirmed upstream image-generation provenance. Proposed non-car revision work remains a separate unstarted proposal. The latest two GLBs are not automatically the previously unidentified separate car experiment; the absent metadata should remain absent.

## A reasonable conventional baseline

The baseline is competent local DCC preparation of the supplied asset under the same declared camera/use contract. It may keep an irregular triangulated shell if it performs adequately; it may locally remesh or remodel the door when that is simpler. It must preserve the native appearance where no change is needed and record each intentional alteration. No full-car replacement, downloaded clean model or expensive reconstruction campaign is needed.

First establish a neutral **import/reopen control**: show the raw GLB with its native UV/PBR, import into the target DCC, save/reopen and re-export/reload without authoring. Match camera, exposure, lights and material interpretation as far as possible. Retain native and roundtrip images; record importer-changed face counts separately from appearance. Do not begin with flattening to vertex colors, global remeshing or a uniform new material. If WebP must be converted for tooling, preserve originals and record decoded-image/content behavior; encoded-byte equality is not required for a different image container.

Then author the specified door using the easiest credible conventional route supported by inspection: asset-specific selection/cut, preservation or transfer of exterior UVs, coherent frame/glass/handle region, local edge/lining/jamb and cavity completion, and a documented plausible hinge. Any missing handle/lining/interior is an authored completion, not recovered truth. Preserve body/fender/wheel placement. Full quad retopology, watertightness and an automated segmenter are not prerequisites unless a measured operation needs them.

Use local remeshing/manual boundary correction as part of this baseline when justified. If a custom script handles only one planar convex polygon and that selection visibly fails, a comparison against that script alone is too weak to support an automation/research claim. Conversely, an unresolved problem at the chosen budget is still a useful bounded observation; it need not trigger repeated repairs.

For the broader artist-use question, image cards and other simple representations are appropriate competitors **only for a use they can satisfy**, such as fixed-view layout. A single image card does not satisfy an independently opening door with exposed edge/cabin and nearby camera motion. No need to implement that irrelevant comparator for this inherited door test. Do not invent a mesh requirement for a future different use after observing results.

## Proposed bounded decisive experiment (not executed by this reviewer)

**Decision question:** With existing supplied outputs and competent ordinary preparation, does the declared door-opening deliverable become technically usable, and what consequential limitation remains at a documented preparation cost?

1. **Freeze evidence/contract.** Preserve A and B with hashes, record unknown provenance and use the existing view/door requirements. Parent's initial views should determine actual coordinate frame and plausible hinge, not old coordinates. Inspect both raw assets before interpreting a result as a model property.
2. **Complete the material-preserving control above.** Resolve at most one identified import/material problem before interpreting generator quality. Retain failures. If compatibility remains blocked, report that stage; no geometry-quality conclusion follows.
3. **Run the same conventional preparation policy for A and B where feasible.** A transparent proposed cap is **45 minutes of active agent preparation per asset**, plus one shared viewer/import setup, with **one evidence-directed local correction** after initial saved-pose inspection. This is a proposed resource bound, not observed human effort or a universal artist threshold. Log actions, start/stop times and rendering/waiting separately. If only one candidate can be authored, choose A by filename order before inspecting authoring outcomes, show B's raw inspection, and restrict the authored conclusion to A. Do not switch silently to the prettier result.
4. **Exercise saved deliverables.** Reopen the exported GLB/scene and verify 0/30/60° and a continuous open→close trajectory, fixed body transforms, coherent moving assembly and return to closed. View same-camera raw, closed authored, intermediate/open and exposed-edge/cabin close-up at the declared resolution. A world transform/slider check supplements these views; it does not replace them. Independent review should inspect the actual saved output, including the worst declared view.
5. **Report a small outcome table.** Per asset: raw appearance under declared views; roundtrip appearance; intended-door selection; aperture/edge/lining/interior plausibility; visible tearing/intersection during motion; closed appearance retained; exported control works; preparation interventions/time; remaining defects. Use pass/fail/uncertain with evidence, not one aggregate score that hides a critical failure. Assistant-only judgment is a technical screen; no artist acceptance, human labor saving or reliability estimate is measured.

If raw appearance clearly cannot satisfy the hero/side task without global remodeling, still separate useful local articulation evidence from the unrepaired global appearance failure. Do not perform a full reconstruction merely to force a positive demo. If raw appearance is good and authoring introduces artifacts, identify the particular intervention and its simplest ordinary correction before attributing failure to generation.

## Stop rule and research implications

- **Conventional path succeeds:** retain/deliver the asset and recipe. If no consequential quality–cost residual remains, close this particular method-gap formulation as engineering. This does not close all research on generated artist assets.
- **Local residual survives the budget:** stop the bounded authoring attempt and classify it (source appearance, display/import, selection, completion, control/export, or unknown/mixed), preserving failed states. One weak cut or unknown runtime is not evidence of intrinsic inability. Do not infer that spending more time would definitely fail or definitely solve it.
- **Global appearance dominates:** report that this sample misses this CGI target and whether lower-demand uses remain plausible. No new generator campaign or broad body remodel in this phase.
- **Candidate difference:** if A and B behave differently, describe it as variation between supplied outputs with unknown settings. No seed/resolution effect, causal generator attribution or reliability proportion follows from two files.
- **Research continuation:** only a consequential residual, a strong ordinary baseline, and a concrete intervention with a falsifiable expected benefit justify another prototype. Confirm later on prospectively chosen assets/operations with the relevant cheapest competitor and a real consumer. A small useful cost/quality improvement may suffice; a dramatic topology failure is not required.

## Evidence references

Current phase (relative to its root):

- `config/INHERITED_AUTHORING_INTENT.md`, especially lines 3–11.
- `inputs/PROVENANCE.json`; `README.md`.
- `inputs/sample_2026-10-09T183055.354.glb` (A), SHA-256 `36c45359ff5fb8b8df0a421f1102598554b9070bc86f0a5e28eee82da3585daa`.
- `inputs/sample_2026-10-09T183324.855.glb` (B), SHA-256 `945781b608e56d99842d7c403252647bf17a7c82b4697f28dcbdb712c39b345a`.
- `research/brief_review/metadata_observations.json` contains this reviewer's direct header/material observations and rehashed source identities.

Historical evidence inspected (absolute paths):

- `/workspace/image_to_usable_car_probe_20261007/inputs/CODEX_IMAGE_TO_USABLE_CAR_PROBE_2026-10-06.md`, lines 4–25.
- `/workspace/image_to_usable_car_probe_20261007/source/cut_door.py`, lines 13–36, 50–65, 85–92.
- `/workspace/image_to_usable_car_probe_20261007/source/author_car.py`, lines 11–22, 27–57, 58–65.
- `/workspace/image_to_usable_car_probe_20261007/IMAGE_TO_USABLE_CAR_REPORT.md`, lines 3–29.
- `/workspace/image_to_usable_car_probe_20261007/logs/authoring-revisions.md`, lines 3–7.
- `/workspace/image_to_usable_car_probe_20261007/research/independent_raw_visual_review.md`, lines 3–22 (attributed visual review, not independently re-rendered here).
- `/workspace/CVPR_3D/trellis2_car_followup_20261009/FINAL_REPORT.md` and `SECRETARY_HANDOFF.md`.
- `/workspace/CVPR_3D/trellis2_route_resolution_20261009/FINAL_REPORT.md` and `SECRETARY_HANDOFF.md`.
- `/workspace/CVPR_3D/research_decision_delivery_20261009/RESEARCH_DECISION.md`, especially lines 14–23, 47–75, and `SECRETARY_HANDOFF.md`.
