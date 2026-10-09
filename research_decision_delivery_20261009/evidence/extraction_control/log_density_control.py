"""One added conventional comparator: interpolate log density on original edges.

Uses existing endpoint densities; one joint density/RGB query per new vertex.
Reuses all original/native/bisection images. The three cases were already explored
before this baseline was selected; they are not prospective validation cases.
"""
import refine_edges as r
import time, json
import numpy as np
import torch
import trimesh
from PIL import Image, ImageDraw

def main():
    results=json.loads((r.OUT/'results.json').read_text())
    decoder,renderer,car_latent=r.load_field()
    assert renderer.cfg.density_activation=='trunc_exp'
    report={'method':'t=(log(25)-log(d0))/(log(d1)-log(d0)), clipped to verified original edge bracket; query fresh RGB and density once per vertex.',
        'additional_encoder_calls':0,'additional_dense_grids':0,
        'prospective_validation':False,'cases_already_explored_before_baseline_selected':True,
        'density_activation':renderer.cfg.density_activation,'threshold':r.THRESHOLD,'faces_unchanged':True,'cases':{}}
    for name,case in results['cases'].items():
        out=r.OUT/name;z=np.load(out/'edge_refinement.npz')
        latent=car_latent if name=='car' else torch.load(case['source_latent'],map_location='cpu',weights_only=True)[0]
        raw=trimesh.load(case['source_mesh'],force='mesh',process=False)
        d0,d1=z['density_start'].astype(np.float64),z['density_end'].astype(np.float64)
        assert np.all(d0>0)&np.all(d1>0)&np.all(z['valid'])
        start=time.monotonic()
        t=(np.log(r.THRESHOLD)-np.log(d0))/(np.log(d1)-np.log(d0))
        assert np.all(np.isfinite(t))&np.all(t>=-1e-12)&np.all(t<=1+1e-12)
        t=np.clip(t,0,1)
        vertices=(z['edge_start'].astype(np.float64)*(1-t[:,None])+z['edge_end'].astype(np.float64)*t[:,None]).astype(np.float32).astype(np.float64)
        position_seconds=time.monotonic()-start
        density,colors=r.query(renderer,decoder,latent,vertices)
        method_seconds=time.monotonic()-start
        colors8=np.round(np.clip(colors,0,1)*255).astype(np.uint8)
        mesh=trimesh.Trimesh(vertices=vertices,faces=z['faces'].copy(),vertex_colors=colors8,process=False)
        mesh.export(out/'log_linear.glb')
        geometry,flips=r.geometry_report(raw,mesh)
        displacement=np.linalg.norm(vertices-z['original_vertices'],axis=1)
        vs_bisection=np.linalg.norm(vertices-z['refined_vertices'],axis=1)
        entry={'position_formula_seconds':position_seconds,'position_and_joint_rgb_density_query_seconds':method_seconds,
            'field_query_points':len(vertices),'bisection_field_query_points_excluding_shared_endpoints':len(vertices)+sum(it['evaluated'] for it in case['bisection_trace']),
            'bisection_query_and_rgb_seconds':case['refinement_query_and_rgb_seconds'],
            'density':r.summary(density),'density_abs_residual':r.summary(np.abs(density-r.THRESHOLD)),
            'displacement_vs_raw':r.summary(displacement),'displacement_vs_bisection':r.summary(vs_bisection),
            'geometry':geometry,'views':{}}
        np.savez_compressed(out/'log_linear.npz',vertices=vertices,faces=z['faces'],rgb=colors,density=density,t=t,displacement_vs_raw=displacement,displacement_vs_bisection=vs_bisection)
        rows={key:[] for key in ['Native field','Original MC density','Log-density linear','10-step bisection','Original clay','Log-density clay','Bisection clay']}
        for az in r.VIEWS:
            view=np.load(out/f'render_arrays_az{az:03}.npz')
            native,a,b=view['native'],view['original_rgb'],view['refined_rgb']
            rgb,depth,normal=r.raster(vertices,z['faces'],colors8.astype(np.float64)/255,*r.camera(az,size=r.PIXELS))
            mask=np.isfinite(depth)&np.isfinite(view['original_depth'])&np.isfinite(view['refined_depth'])
            all_mask=np.ones(mask.shape,bool)
            log_mask=np.isfinite(depth);raw_mask=np.isfinite(view['original_depth']);bis_mask=np.isfinite(view['refined_depth'])
            m={'common_three_way_mask_pixels':int(mask.sum()),
                'raw_vs_native_common_mask':r.image_metrics(a,native,mask),
                'log_vs_native_common_mask':r.image_metrics(rgb,native,mask),
                'bisection_vs_native_common_mask':r.image_metrics(b,native,mask),
                'raw_vs_native_full':r.image_metrics(a,native,all_mask),
                'log_vs_native_full':r.image_metrics(rgb,native,all_mask),
                'bisection_vs_native_full':r.image_metrics(b,native,all_mask),
                'log_vs_raw_common_mask':r.image_metrics(rgb,a,mask),
                'log_vs_bisection_common_mask':r.image_metrics(rgb,b,mask),
                'silhouette_IoU_vs_raw':float((log_mask&raw_mask).sum()/(log_mask|raw_mask).sum()),
                'silhouette_IoU_vs_bisection':float((log_mask&bis_mask).sum()/(log_mask|bis_mask).sum())}
            m['log_relative_MAE_improvement']=1-m['log_vs_native_common_mask']['MAE']/m['raw_vs_native_common_mask']['MAE']
            m['bisection_relative_MAE_improvement']=1-m['bisection_vs_native_common_mask']['MAE']/m['raw_vs_native_common_mask']['MAE']
            m['fraction_of_bisection_MAE_gain_retained_by_log']=(m['raw_vs_native_common_mask']['MAE']-m['log_vs_native_common_mask']['MAE'])/(m['raw_vs_native_common_mask']['MAE']-m['bisection_vs_native_common_mask']['MAE'])
            entry['views'][str(az)]=m
            shaded=r.clay(rgb,depth,normal,az)
            r.save_rgb(out/f'log_linear_rgb_az{az:03}.png',rgb)
            r.save_rgb(out/f'log_linear_clay_az{az:03}.png',shaded)
            hrgb,hdepth,hnorm=r.raster(vertices,z['faces'],np.full((len(vertices),3),.7),*r.camera(az,size=480))
            r.save_rgb(out/f'log_linear_clay480_az{az:03}.png',r.clay(hrgb,hdepth,hnorm,az))
            np.savez_compressed(out/f'log_render_arrays_az{az:03}.npz',rgb=rgb,depth=depth,normals=normal)
            clay_a=r.clay(a,view['original_depth'],view['original_normals'],az)
            clay_b=r.clay(b,view['refined_depth'],view['refined_normals'],az)
            for key,img in zip(rows,[native,a,rgb,b,clay_a,shaded,clay_b]):rows[key].append(img)
        def weighted(key):
            return sum(v[key]['MAE']*v[key]['pixels'] for v in entry['views'].values())/sum(v[key]['pixels'] for v in entry['views'].values())
        aggregate={key:weighted(key) for key in ['raw_vs_native_common_mask','log_vs_native_common_mask','bisection_vs_native_common_mask','log_vs_bisection_common_mask','raw_vs_native_full','log_vs_native_full','bisection_vs_native_full']}
        raw_mae,log_mae,bis_mae=[aggregate[f'{key}_vs_native_common_mask'] for key in ('raw','log','bisection')]
        aggregate['log_relative_MAE_improvement']=1-log_mae/raw_mae
        aggregate['bisection_relative_MAE_improvement']=1-bis_mae/raw_mae
        aggregate['fraction_of_bisection_MAE_gain_retained_by_log']=(raw_mae-log_mae)/(raw_mae-bis_mae)
        entry['aggregate']=aggregate
        tile=240;label=185;header=30
        sheet=Image.new('RGB',(label+tile*len(r.VIEWS),header+tile*len(rows)),'white');draw=ImageDraw.Draw(sheet)
        for i,az in enumerate(r.VIEWS):draw.text((label+tile*i+75,8),f'azimuth {az}',fill='black')
        for j,(key,images) in enumerate(rows.items()):
            draw.text((8,header+j*tile+100),key,fill='black')
            for i,img in enumerate(images):
                im=Image.fromarray(np.round(np.clip(img,0,1)*255).astype(np.uint8)).resize((tile,tile))
                sheet.paste(im,(label+i*tile,header+j*tile))
        sheet.save(out/'three_way_comparison.png')
        loaded=trimesh.load(out/'log_linear.glb',force='mesh',process=False)
        entry['export_verified_exact']=bool(np.array_equal(loaded.vertices,vertices)&np.array_equal(loaded.faces,z['faces'])&np.array_equal(loaded.visual.vertex_colors[:,:3],colors8))
        assert entry['export_verified_exact']
        report['cases'][name]=entry
        (r.OUT/'log_density_results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'case':name,'residual_mean':entry['density_abs_residual']['mean'],'method_seconds':method_seconds,**aggregate}),flush=True)

if __name__=='__main__':main()
