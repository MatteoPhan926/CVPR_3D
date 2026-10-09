"""Checks saved outputs and runs render-only crossed position/RGB controls."""
import refine_edges as r
import json
import numpy as np
import trimesh
from PIL import Image
from tsr.utils import get_spherical_cameras

def main():
    results=json.loads((r.OUT/'results.json').read_text())
    report={'additional_encoder_calls':0,'additional_field_queries':0,'cases':{},
        'crossed_control_note':'RGB labels remain attached to corresponding vertices. Mixed combinations isolate rendering sensitivity; they are not independent reconstructed assets.'}
    ro,rd=get_spherical_cameras(6,20,1.9,40,r.PIXELS,r.PIXELS)
    cameras={}
    for i,az in enumerate(r.VIEWS):
        cam,right,up,look,size,focal=r.camera(az,size=r.PIXELS)
        yy,xx=np.mgrid[:size,:size]
        analytic=look+((xx+.5-size/2)/focal)[...,None]*right-((yy+.5-size/2)/focal)[...,None]*up
        analytic/=np.linalg.norm(analytic,axis=-1,keepdims=True)
        cameras[str(az)]={'max_ray_direction_component_error':float(np.max(np.abs(analytic-rd[i].numpy()))),
            'max_camera_origin_component_error':float(np.max(np.abs(cam-ro[i].numpy())))}
    report['camera_consistency']=cameras
    lines=['case\tview\traw_geometry_raw_rgb\traw_geometry_refined_rgb\trefined_geometry_raw_rgb\trefined_geometry_refined_rgb']
    for name,case in results['cases'].items():
        out=r.OUT/name
        z=np.load(out/'edge_refinement.npz')
        original=trimesh.load(out/'original_control.glb',force='mesh',process=False)
        refined=trimesh.load(out/'refined.glb',force='mesh',process=False)
        rgb1=np.round(np.clip(z['refined_rgb'],0,1)*255).astype(np.uint8)
        checks={'source_mesh_hash_unchanged':r.digest(r.Path(case['source_mesh']))==case['source_mesh_sha256'],
            'source_latent_hash_unchanged':r.digest(r.Path(case['source_latent']))==case['source_latent_sha256'],
            'control_vertices_exact':bool(np.array_equal(original.vertices,z['original_vertices'])),
            'control_faces_exact':bool(np.array_equal(original.faces,z['faces'])),
            'control_rgb_exact':bool(np.array_equal(original.visual.vertex_colors[:,:3],z['original_rgb'])),
            'refined_vertices_exact':bool(np.array_equal(refined.vertices,z['refined_vertices'])),
            'refined_faces_exact':bool(np.array_equal(refined.faces,z['faces'])),
            'refined_rgb_exact':bool(np.array_equal(refined.visual.vertex_colors[:,:3],rgb1)),
            'refined_vertices_within_original_grid_edge':bool(np.all(z['refined_vertices']>=np.minimum(z['edge_start'],z['edge_end'])-1e-7)&np.all(z['refined_vertices']<=np.maximum(z['edge_start'],z['edge_end'])+1e-7))}
        assert all(checks.values()),checks
        controls={}
        pixel_total=sum(v['original_vs_native_common_mask']['pixels'] for v in case['views'].values())
        def weighted(key):
            return sum(v[key]['MAE']*v[key]['pixels'] for v in case['views'].values())/sum(v[key]['pixels'] for v in case['views'].values())
        aggregate={key:weighted(key) for key in ['original_vs_native_common_mask','refined_vs_native_common_mask','raw_vs_refined_common_mask','original_vs_native_full','refined_vs_native_full']}
        aggregate['relative_common_mask_MAE_improvement']=1-aggregate['refined_vs_native_common_mask']/aggregate['original_vs_native_common_mask']
        aggregate['relative_full_image_MAE_improvement']=1-aggregate['refined_vs_native_full']/aggregate['original_vs_native_full']
        for az in r.VIEWS:
            view=np.load(out/f'render_arrays_az{az:03}.npz')
            mask=np.isfinite(view['original_depth'])&np.isfinite(view['refined_depth'])
            native=view['native']
            combo={}
            for geometry,verts in [('raw',z['original_vertices']),('refined',z['refined_vertices'])]:
                for color,colors in [('raw',z['original_rgb']),('refined',rgb1)]:
                    key=f'{geometry}_geometry_{color}_rgb'
                    rgb,depth,normal=r.raster(verts,z['faces'],colors.astype(np.float64)/255,*r.camera(az,size=r.PIXELS))
                    combo[key]=r.image_metrics(rgb,native,mask)
                    if geometry!=color:
                        r.save_rgb(out/f'crossed_{key}_az{az:03}.png',rgb)
            controls[str(az)]=combo
            lines.append('\t'.join([name,str(az)]+[str(combo[key]['MAE']) for key in ['raw_geometry_raw_rgb','raw_geometry_refined_rgb','refined_geometry_raw_rgb','refined_geometry_refined_rgb']]))
        if name=='car':
            checks['native_png_exact_to_prior_run']=all(np.array_equal(np.array(Image.open(out/f'native_az{az:03}.png')),np.array(Image.open(r.GEN/f'native_field_az{az:03}.png'))) for az in r.VIEWS)
            checks['raw_raster_png_exact_to_prior_run']=all(np.array_equal(np.array(Image.open(out/f'original_rgb_az{az:03}.png')),np.array(Image.open(r.GEN/f'original_r256_t25_flat_az{az:03}.png'))) for az in r.VIEWS)
            assert checks['native_png_exact_to_prior_run'] and checks['raw_raster_png_exact_to_prior_run']
        aggregate['residual_reduction_factor']=case['original_density_abs_residual']['mean']/case['refined_density_abs_residual']['mean']
        aggregate['minimum_silhouette_IoU']=min(v['silhouette_IoU'] for v in case['views'].values())
        report['cases'][name]={'checks':checks,'aggregate':aggregate,'crossed_controls':controls}
    (r.OUT/'verification_and_aggregate.json').write_text(json.dumps(report,indent=2)+'\n')
    (r.OUT/'crossed_controls.tsv').write_text('\n'.join(lines)+'\n')
    print(json.dumps({name:case['aggregate'] for name,case in report['cases'].items()},indent=2))

if __name__=='__main__':main()
