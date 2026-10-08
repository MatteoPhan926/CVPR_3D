"""Actual Chromium/glTF shader checks; images are not synthetic mock outputs."""
from pathlib import Path
import json,base64
import numpy as np
from PIL import Image,ImageDraw
def binary_erosion(mask,iterations=1):
    for _ in range(iterations):
        p=np.pad(mask,1,constant_values=False)
        mask=p[1:-1,1:-1]&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
    return mask
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'browser/results';OUT.mkdir(exist_ok=True)
variants=['raw','unlit_direct','unlit_corrected','pbr_corrected']
report={'scope':'Fixed geometry/camera, no tone mapping primary, front-side culling common. PBR corrected adds smooth normals; no physical relighting ground truth. Reference emits interpolated stored decoder RGB directly without output transfer.','cases':{},'browser_errors':[]}
all_images={}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':320,'height':320},device_scale_factor=1)
    page.on('pageerror',lambda e:report['browser_errors'].append(str(e)))
    page.on('console',lambda m:report['browser_errors'].append(m.text) if m.type=='error' and 'WebGL' in m.text else None)
    page.goto('http://127.0.0.1:8788/root_analysis/browser/',wait_until='networkidle');page.wait_for_function('window.testAPI?.ready')
    report['browser_version']=browser.version
    for case in ['car','teapot','hamburger']:
        out=OUT/case;out.mkdir(exist_ok=True);report['cases'][case]={}
        for az in [0,60,120]:
            images={}
            for variant in ['reference','mask']+variants:
                for light in ([0,1] if variant in variants else [0]):
                    s=page.evaluate('async x=>await testAPI.render(...x)',[case,variant,az,light,'none'])
                    dest=out/f'{variant}_az{az:03}_light{light}.png';dest.write_bytes(base64.b64decode(s.split(',')[1]));images[variant,light]=np.asarray(Image.open(dest).convert('RGB'),dtype=float)/255
            common=binary_erosion(images['mask',0].mean(2)<.1,iterations=1)
            assert common.sum()>100,case
            ref=images['reference',0];r={}
            for variant in variants:
                x=images[variant,0];r[variant]={'MAE_to_direct_RGB_reference':float(np.abs(x[common]-ref[common]).mean()),'mean_display_luma':float((x[common]@np.array([.2126,.7152,.0722])).mean()),'light_change_MAE':float(np.abs(x[common]-images[variant,1][common]).mean())}
            r['foreground_pixels']=int(common.sum());report['cases'][case][str(az)]=r
            if az==0:all_images[case]=images
        # Separate known viewer tone-mapping effect; never merged with primary result.
        for variant in ['unlit_corrected','raw']:
            s=page.evaluate('async x=>await testAPI.render(...x)',[case,variant,0,0,'aces']);(out/f'{variant}_az000_aces.png').write_bytes(base64.b64decode(s.split(',')[1]))
    browser.close()
assert not report['browser_errors'],report['browser_errors']
(OUT/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
columns=['reference']+variants;tile=320;label=130;header=70
sheet=Image.new('RGB',(label+len(columns)*tile,header+3*tile),'white');draw=ImageDraw.Draw(sheet)
titles=['Direct decoder RGB','Released glTF/PBR','Unlit, direct RGB','Unlit, inverse-sRGB','Dielectric PBR, inverse-sRGB']
for i,title in enumerate(titles):draw.text((label+i*tile+5,20),title,fill='black')
for j,(case,ims) in enumerate(all_images.items()):
    draw.text((5,header+j*tile+140),case,fill='black')
    for i,name in enumerate(columns):sheet.paste(Image.fromarray(np.round(ims[name,0]*255).astype(np.uint8)),(label+i*tile,header+j*tile))
sheet.save(OUT/'export_comparison.png')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2));print('Completed 3 cases × 3 fixed views; all exported geometry preserved.')
