# Supplied GLB integrity and unmodified Blender roundtrip

Originals checkpoint gate was checked before processing: `../../checkpoints/01_originals.verification.json` exists and reports `externally_verified: true`. Original GLBs were read only, and their SHA-256 hashes remained unchanged. This directory contains fresh outputs and all local probe sources/logs. No model generation, network request, paid action, render, or authoring edit was performed by these probes.

User provenance update supplied by the parent: these are HF-direct trials, with 512 and 1536 tested. File-to-resolution mapping, seeds, decimation settings, and original versus background-removed conditioning-image association remain unknown. These files are therefore not a controlled resolution comparison. No inference is made from a failed Randomize Seed screenshot.

| Measured property | `183055.354` (A) | `183324.855` (B) |
|---|---:|---:|
| Native indexed vertices | 183,392 | 178,694 |
| Native triangles | 291,603 | 276,585 |
| Native glTF XYZ extents | 1.001770 × 0.364140 × 0.493419 | 0.422687 × 0.342471 × 0.998235 |
| Meshes / primitives / materials | 1 / 1 / 1 | 1 / 1 / 1 |
| Required texture extension | EXT_texture_webp | EXT_texture_webp |
| Original validator errors / warnings | 0 / 0 | 0 / 0 |
| Exact-position diagnostic components with faces | 11 | 3 |
| Largest diagnostic component area fraction | 99.4810% | 99.9068% |
| Zero geometric-area triangles | 1 | 1 |
| Zero UV-area triangles | 7 | 44 |
| Geometric area fraction with zero UV area | 0.00001214% | 0.00014690% |

Both contain native TEXCOORD_0 and NORMAL attributes, one embedded 2048×2048 WebP base-color texture and one embedded 2048×2048 WebP metallic-roughness texture. Their material uses texture-driven metallic and roughness values, OPAQUE alpha, and one-sided rendering. There are no animations, skins, morph targets, authored part names, separate material regions, or normal maps. The metadata identifies a trimesh exporter, which does not establish generation provenance. Extents are asset coordinates, not a verified physical scale.

Khronos glTF Validator 2.0.0-dev.3.10 found no errors or warnings. The four original hints per file only concern omitted bufferView.target. Each exported copy validates with zero errors, warnings, infos, or hints.

## Actual import, export, and fresh-process reimport control

Blender 4.3.2 imported both originals, exported unmodified fresh GLBs, then imported those outputs in separate fresh Blender processes. Each process used one CPU thread and no rendering. Material graphs connected base color as sRGB, and metallic-roughness as Non-Color with blue→metallic and green→roughness. Both images loaded and remained packed. The exported material omits some explicit default values; effective material factors, alpha mode, sidedness, and texture references are identical.

The comparison expands indexed attributes into ordered triangle corners. Both files preserve **every ordered POSITION and TEXCOORD_0 value exactly**, and retain their triangle counts. This is stronger evidence than equality of an oriented triangle multiset: there is no observed position, winding, topology-by-position, or UV loss in this roundtrip. Both encoded WebP payloads, their decoded RGBA pixels, and effective material values are identical. AUTO export preserved WebP and still requires EXT_texture_webp; it did not transcode to PNG or produce a fallback for consumers lacking WebP support.

Normals are not bit-identical. Median angular drift is 0.002565° (A) / 0.002621° (B), and the 99th percentile is 0.01814° / 0.02006°. Only 33 / 21 corners change by more than 0.1°, on faces totaling 0.002499% / 0.001215% of geometric surface area. A's maximum 46.83° change occurs on its zero-area triangle; B's maximum 26.33° also occurs on its zero-area triangle. A has one corner above 1° on zero area; B has three corners above 1° on faces totaling 0.00000847% of surface area. Exported vertex counts increase to 183,665 / 181,275, consistent with additional attribute splits rather than added geometric faces. The control measures drift, and does not by itself prove rendered perceptual equivalence.

The results do not support broad geometry or texture corruption during this tested Blender path as the primary explanation for defects already visible in the assets. A visual artifact confined to pathological slivers could still require a targeted normal check.

## Topology interpretation and downstream limits

Native index graphs contain 2,647 / 3,905 components and 71,747 / 77,605 boundary edges. These counts must not be interpreted as thousands of disconnected physical fragments: duplicated positions at UV or normal seams dominate. A diagnostic exact-position weld reduces the graphs to 11 / 3 components without modifying an output mesh. Under that diagnostic interpretation, there are 172 / 37 edges incident to more than two faces, 12 / 11 duplicate unoriented triangles, and one boundary edge each. Coincident surfaces and degenerate triangles can affect these measures; exact-position welding is not proof of a repairable manifold representation. No mesh was welded or repaired.

The largest component spans the full model in each case and contains 98.7558% / 99.7165% of triangles. Connected-component extraction therefore does not supply semantic parts such as doors. One mesh/material also supplies no native authoring partition. Good file integrity and native PBR do not establish independently editable mechanical parts, thickness, hidden surfaces, pivots, or suitability for articulation.

## Cheap discriminating control

The requested import→unmodified export→fresh reimport control is complete. It retains geometry, UVs and textures, isolating a small normal drift. The next inexpensive discrimination should exercise the chosen concrete authoring task on a copy, holding geometry and native textures fixed: for example, save a reversible face-region selection and assign a local contrasting material, then verify selected versus protected face counts and reimport preservation. Failure to isolate a semantic region would be an authoring/segmentation limitation; successful local appearance editing would still not establish a mechanically valid detachable or articulated part. A new generation call is not needed to perform that control.

Detailed evidence: `*.inspection.json`, `*.validation.json`, `*.geometry.json`, `*.blender_import_export.json`, `*.unmodified_export.reimport.json`, `*.roundtrip_comparison.json`; retained exports: `*.unmodified_export.glb`. Matching `.log` files record commands and return codes. Geometry diagnostics include texture channel distributions, which include atlas padding and should not be read as surface-weighted material estimates.
