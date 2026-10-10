# Selected-surface provenance: source and preparation remain confounded

The executed cut selected 15,064 triangles. Of these, 12,995 are source faces wholly on the moving side (94.2066% of selected area). Another 2,069 are descendants of 1,365 source triangles also represented in the fixed body (5.7934%). These labels are exact source-face bookkeeping from the saved cut arrays, not semantic door ground truth.

By geometric face normal relative to the original outward direction -Y, 41.5903% of selected area has dot >=0.5, 17.8168% lies between -0.5 and +0.5, and 40.5929% has dot <=-0.5. Window tunnels, frame sides and other legitimate door surfaces can face inward or sideways; this is not an automatic deletion criterion. The mix makes a simplistic exterior-skin interpretation inappropriate.

All 1,396 geometric boundary edges lie on clipping planes: 1,086 on the XZ polygon perimeter (81.0408% of boundary length) and 310 on depth Y=-0.100 (18.9592%). Zero off-plane boundary edges were observed. The earlier concern that fixed jamb would include pre-existing open window boundaries was a prospective safeguard, not an observed defect in this cut. A visible window aperture can be a tunnel in a closed mesh and need not have mesh boundary edges.

Actual provenance renders in ../../artifacts/selection_overlay_A show cyan source faces and orange clipped descendants along many irregular exposed silhouettes. The inward-orientation diagnostic uses a different, explicitly recorded +/-0.25 threshold for visual coloring. The large fraction of original area does not prove the visually consequential edge was an intrinsic model defect: a small boundary region can dominate the open-door view.

The partition-only open pose already contains irregular sheets before lining/jamb completion. Thus new lining is not the sole explanation, while source surface geometry, semantic region membership, contour/depth selection and their interaction remain competing explanations. No local face removal, alternative cut, or refined artist cleanup was executed. A stronger conventional workflow may resolve this residual; this screen does not bound its quality or labor.

See selection_provenance.json, summarize_selection.py and door_diagnostic_labels.npz; original cut arrays and source-face IDs remain in artifacts/authoring_A_v1/cut_arrays.npz.
