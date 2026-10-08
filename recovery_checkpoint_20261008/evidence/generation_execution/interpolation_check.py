"""Check MC xyz convention and continuous-field residual on original edges."""
import os
os.environ['OMP_NUM_THREADS']='2';os.environ['MKL_NUM_THREADS']='2'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import json
import numpy as np
import torch
import trimesh
from scipy.spatial import cKDTree
from provenance_check import ROOT,OUT,load_field,summary

def main():
    decoder,renderer,latent=load_field()
    raw=trimesh.load(ROOT/'raw/car_raw.glb',force='mesh',process=False)
    regenerated=trimesh.load(OUT/'r256_t25.glb',force='mesh',process=False)
    distances,mapping=cKDTree(raw.vertices).query(regenerated.vertices)
    original_faces={tuple(sorted(f)) for f in raw.faces}
    regenerated_faces={tuple(sorted(f)) for f in mapping[regenerated.faces]}
    report={'reproduction_order_invariant':{'vertex_nearest_distance':summary(distances),
        'bijective_nearest_vertex_mapping':len(set(mapping.tolist()))==len(raw.vertices),
        'triangle_sets_equal_under_mapping':original_faces==regenerated_faces,
        'corresponding_rgb_exact_fraction':float(np.mean(np.all(regenerated.visual.vertex_colors==raw.visual.vertex_colors[mapping],axis=1)))}}
    v=np.asarray(raw.vertices)
    coords=(torch.linspace(0,1,256)*(2*renderer.cfg.radius)-renderer.cfg.radius).numpy()
    grid=np.load(OUT/'density_grid_256.npy')
    lattice=(v+renderer.cfg.radius)/(2*renderer.cfg.radius)*255
    fraction=np.abs(lattice-np.round(lattice))
    axis=np.argmax(fraction,axis=1)
    edge_lo=np.round(lattice).astype(int)
    edge_lo[np.arange(len(v)),axis]=np.floor(lattice[np.arange(len(v)),axis]).astype(int)
    edge_hi=edge_lo.copy();edge_hi[np.arange(len(v)),axis]+=1
    p0=coords[edge_lo];p1=coords[edge_hi]
    d0=grid[tuple(edge_lo.T)];d1=grid[tuple(edge_hi.T)]
    t=(v[np.arange(len(v)),axis]-p0[np.arange(len(v)),axis])/(p1[np.arange(len(v)),axis]-p0[np.arange(len(v)),axis])
    d_interp=d0*(1-t)+d1*t
    with torch.no_grad():
        density=renderer.query_triplane(decoder,torch.tensor(v,dtype=torch.float32),latent)['density_act'].numpy().ravel()
        # Explicitly query edge endpoints to independently verify indexing.
        ends=renderer.query_triplane(decoder,torch.tensor(np.concatenate([p0,p1]),dtype=torch.float32),latent)['density_act'].numpy().ravel()
    gradients=[]
    for start in range(0,len(v),4096):
        points=torch.tensor(v[start:start+4096],dtype=torch.float32,requires_grad=True)
        q=renderer.query_triplane(decoder,points,latent)['density_act']
        gradients.append(torch.autograd.grad(q.sum(),points)[0].detach().numpy())
    gradients=np.concatenate(gradients)
    report['edge_convention']={'orthogonal_axes_max_lattice_roundoff':summary(np.sort(fraction,axis=1)[:,:2]),
        'endpoint_decoder_vs_grid_absolute_error':summary(np.abs(ends-np.concatenate([d0,d1]))),
        'bracketing_fraction':float(np.mean((d0-25)*(d1-25)<=0)),
        'linear_grid_interpolation_density':summary(d_interp),
        'linear_interpolation_threshold_abs_residual':summary(np.abs(d_interp-25)),
        'continuous_decoder_density':summary(density),
        'continuous_threshold_abs_residual':summary(np.abs(density-25)),
        'density_gradient_norm':summary(np.linalg.norm(gradients,axis=1)),
        'linearized_normal_displacement':summary(np.abs(density-25)/np.linalg.norm(gradients,axis=1)),
        'cell_width':float(coords[1]-coords[0]),
    }
    np.savez_compressed(OUT/'per_vertex_interpolation.npz',vertices=v,axis=axis,edge_lo=edge_lo,edge_hi=edge_hi,edge_start=p0,edge_end=p1,density_start=d0,density_end=d1,t_linear=t,density_linear=d_interp,density_actual=density,density_gradient=gradients,bounds=raw.bounds)
    (OUT/'interpolation_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
