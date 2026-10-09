#!/usr/bin/env python3
"""Recompute report arithmetic from retained JSON only; no model/render calls."""
import argparse,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
E=ROOT/"evidence"
def read(rel):return json.loads((E/rel).read_text())
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",default="DERIVED_SUMMARY_RECOMPUTED.json");args=p.parse_args()
 aggregate=read("extraction_control/verification_and_aggregate.json")
 original=read("extraction_control/results.json")
 cases={}
 for name,item in aggregate["cases"].items():
  views=item["crossed_controls"]
  keys=list(next(iter(views.values())))
  scores={k:sum(v[k]["MAE"]*v[k]["pixels"] for v in views.values())/sum(v[k]["pixels"] for v in views.values()) for k in keys}
  raw=scores["raw_geometry_raw_rgb"];joint=scores["refined_geometry_refined_rgb"]
  assert abs(raw-item["aggregate"]["original_vs_native_common_mask"])<1e-12
  assert abs(joint-item["aggregate"]["refined_vs_native_common_mask"])<1e-12
  measurements=original["cases"][name]
  cases[name]={
   "vertices":measurements["vertices"],"faces":measurements["faces"],
   "native_field_MAE":scores,"joint_relative_MAE_reduction":1-joint/raw,
   "rgb_only_fraction_of_joint_reduction":(raw-scores["raw_geometry_refined_rgb"])/(raw-joint),
   "crossed_control_limit":"Sensitivity comparison, not additive causal attribution; refined RGB still sampled at refined positions.",
   "original_density_residual_mean":measurements["original_density_abs_residual"]["mean"],
   "refined_density_residual_mean":measurements["refined_density_abs_residual"]["mean"],
   "mean_displacement_model_units":measurements["displacement"]["mean"],
   "mean_displacement_fraction_cell":measurements["displacement_fraction_cell_width"]["mean"],
   "refinement_queries_and_rgb_seconds":measurements["refinement_query_and_rgb_seconds"],
   "refinement_and_export_seconds":measurements["refinement_and_export_elapsed_seconds"],
   "minimum_mesh_to_mesh_silhouette_IoU":item["aggregate"]["minimum_silhouette_IoU"],
   "full_image_relative_MAE_reduction":item["aggregate"]["relative_full_image_MAE_improvement"],
   "negative_original_refined_normal_dot_count":measurements["geometry"]["negative_original_refined_normal_dot_count"],
   "faces_array_exact":measurements["geometry"]["faces_array_exact"],
  }
 pairs=read("authoring_attribution/measurements/pixel_metrics.json")["pairs"]
 authoring={key:{view:{"RGB_MAE":v["RGB_MAE_display_0_1"],"silhouette_IoU":v["silhouette_IoU"],"display_luma_ratio":v["mean_luma_b"]/v["mean_luma_a"]} for view,v in pairs[key].items()} for key in ["prior_display_material","flat_partition","smooth_partition","complete_closed_pipeline"]}
 components=read("authoring_attribution/measurements/selection_components.json")
 actual_activation=next(line.split(":",1)[1].strip() for line in (E/"checkpoint_configuration/checkpoint_config.yaml").read_text().splitlines() if line.strip().startswith("density_activation:"))
 assert actual_activation=="exp"
 forward=read("root_analysis/saved_forward_reproduction.json")
 assert forward["exact_tensor_equal"] and forward["max_abs_error"]==0.0
 inputs=["extraction_control/verification_and_aggregate.json","extraction_control/results.json","authoring_attribution/measurements/pixel_metrics.json","authoring_attribution/measurements/selection_components.json","root_analysis/saved_forward_reproduction.json","checkpoint_configuration/checkpoint_config.yaml"]
 out={"created_at_utc":datetime.now(timezone.utc).isoformat(),"operation":"Arithmetic and assertions over retained JSON/config only","new_encoder_calls":0,"new_field_queries":0,"new_renders":0,"extraction_cases":cases,"authoring":authoring,"lower_selection_area_fraction":components[1]["area"]/sum(c["area"] for c in components),"checkpoint_density_activation":actual_activation,"saved_forward_replay":forward,"metric_limits":["Three already explored objects, three 160x160 views each for extraction, one model; views are not independent objects.","Common mask is intersection of original/refined raster masks, not ground-truth support.","Native-field reference is internal; no geometry truth or artist acceptance measured.","Signed mesh integral values on non-watertight meshes are not physical volume."],"input_sha256":{rel:hashlib.sha256((E/rel).read_bytes()).hexdigest() for rel in inputs}}
 target=ROOT/args.output
 with target.open("x") as f:json.dump(out,f,indent=2)
 print(json.dumps({"output":str(target),"activation":actual_activation,"cases":{k:{"MAE":v["native_field_MAE"],"relative_reduction":v["joint_relative_MAE_reduction"]} for k,v in cases.items()}},indent=2))
if __name__=="__main__":main()

