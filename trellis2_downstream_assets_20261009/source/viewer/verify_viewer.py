#!/usr/bin/env python3
"""Verify a standalone HTML opened directly by Chromium, with network access blocked."""
import argparse, hashlib, json, math, time
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser();p.add_argument('--html',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
p.add_argument('--chromium',default='/usr/bin/chromium');args=p.parse_args()
assert args.html.is_file()
args.output.mkdir(parents=True,exist_ok=False)
errors=[];requests=[];console_errors=[];snapshots={};states={}
html_hash=hashlib.sha256(args.html.read_bytes()).hexdigest()
def maximum_matrix_delta(a,b):
    return max(abs(x-y) for x,y in zip(a['matrixWorld'],b['matrixWorld']))
def index(rows):return {r['name']:r for r in rows}
def angular_difference(q0,q1):
    dot=abs(sum(a*b for a,b in zip(q0,q1)));norm=math.sqrt(sum(a*a for a in q0)*sum(a*a for a in q1))
    return math.degrees(2*math.acos(min(1,dot/norm)))
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(executable_path=args.chromium,headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda e:console_errors.append(e.text) if e.type=='error' else None)
    def route(request):
        if request.request.url.startswith(('http:','https:')):
            requests.append(request.request.url);request.abort()
        else:request.continue_()
    page.route('**/*',route)
    page.goto(args.html.resolve().as_uri(),wait_until='load',timeout=90000)
    page.wait_for_function('window.assetViewer && assetViewer.getState().ready',timeout=90000)
    assert not page.locator('#doorSlider').is_disabled()
    for angle,label in [(0,'closed'),(30,'half'),(60,'open')]:
        page.locator('#doorSlider').evaluate('(element, value) => { element.value=String(value); element.dispatchEvent(new Event("input", {bubbles:true})); }',angle)
        state=page.evaluate('assetViewer.getState()');assert abs(state['angle']-angle)<1e-8
        snapshots[label]=index(page.evaluate('assetViewer.getTransforms()'));states[label]=state
        page.screenshot(path=str(args.output/f'{label}.png'))
    initial=states['closed'];assert initial['animation'] and initial['openingSeconds']==2
    hinge=next(name for name in snapshots['closed'] if 'FrontDoor_Control' in name)
    body=next(name for name in snapshots['closed'] if 'Generated' in name and 'exterior' in name and 'fixed' in name)
    door=next(name for name in snapshots['closed'] if 'Generated' in name and 'front' in name and 'door' in name)
    moving=[];fixed=[]
    for name,node in snapshots['closed'].items():
        (moving if maximum_matrix_delta(node,snapshots['open'][name])>1e-7 else fixed).append(name)
    assert hinge in moving and door in moving and body in fixed,(hinge,body,door,moving,fixed)
    angles={}
    for label,expected in [('half',30),('open',60)]:
        measured=angular_difference(snapshots['closed'][hinge]['quaternion'],snapshots[label][hinge]['quaternion'])
        assert abs(measured-expected)<.01,(label,measured)
        angles[label]=measured
        assert maximum_matrix_delta(snapshots['closed'][body],snapshots[label][body])<1e-9
    page.locator('[data-view="side"]').click();assert page.evaluate('assetViewer.getState().view')=='side'
    page.screenshot(path=str(args.output/'open_side.png'))
    page.locator('#resetButton').click();reset=index(page.evaluate('assetViewer.getTransforms()'))
    reset_delta=max(maximum_matrix_delta(node,reset[name]) for name,node in snapshots['closed'].items())
    assert reset_delta<1e-9
    assert page.evaluate('assetViewer.getState().view')=='hero'
    # Real-time playback crosses the apex and returns toward closed; no test-only time override.
    started=time.monotonic();page.locator('#playButton').click()
    page.wait_for_function('assetViewer.getState().playing && assetViewer.getState().angle > 10 && assetViewer.getState().direction === 1',timeout=10000)
    opening=page.evaluate('assetViewer.getState()')
    page.wait_for_function('assetViewer.getState().playing && assetViewer.getState().direction === -1 && assetViewer.getState().angle < 50',timeout=10000)
    closing=page.evaluate('assetViewer.getState()')
    page.wait_for_function('assetViewer.getState().direction === 1 && assetViewer.getState().angle < 15',timeout=10000)
    cycle_seconds=time.monotonic()-started
    page.locator('#playButton').click();paused=page.evaluate('assetViewer.getState()')
    assert not paused['playing'];page.wait_for_timeout(180)
    assert page.evaluate('assetViewer.getState().angle')==paused['angle']
    page.locator('#closedButton').click();assert page.evaluate('assetViewer.getState().angle')==0
    page.locator('#openButton').click();assert page.evaluate('assetViewer.getState().angle')==60
    page.locator('#resetButton').click()
    materials=page.evaluate('assetViewer.getMaterials()')
    native=[m for m in materials if m['baseColorTexture'] and m['roughnessTexture'] and m['metallicTexture']]
    assert native,'Native base-color + metallic/roughness material missing'
    assert all(m['baseColorSpace']=='srgb' and m['roughnessColorSpace']=='' for m in native),native
    assert not errors and not console_errors and not requests,(errors,console_errors,requests)
    # Pixel evidence excludes the control panel and fixed labels.
    closed=np.asarray(Image.open(args.output/'closed.png').convert('RGB'))[190:830,50:1100]
    opened=np.asarray(Image.open(args.output/'open.png').convert('RGB'))[190:830,50:1100]
    changed=np.any(abs(closed.astype(np.int16)-opened.astype(np.int16))>8,axis=-1)
    changed_pixels=int(changed.sum());assert changed_pixels>300,'No meaningful visual response to the door slider'
    assert len(np.unique(closed.reshape(-1,3),axis=0))>200,'Viewport appears blank'
    report={'status':'passed','html':str(args.html),'html_sha256':html_hash,'browser':browser.version,
      'opened_via':'file://','external_network_requests':requests,'javascript_errors':errors,'console_errors':console_errors,
      'controls_checked':['0/30/60-degree slider','open/close playback and reversal','pause','closed','open','reset','side camera'],
      'measured_hinge_angles_degrees':angles,'moving_nodes':moving,'fixed_nodes':fixed,'fixed_body':body,
      'reset_max_matrix_delta':reset_delta,'first_cycle_observed_seconds_including_browser_calls':cycle_seconds,
      'opening_state':opening,'closing_state':closing,'materials':materials,'initial_state':initial,
      'viewport_pixels_changing_above_8_channel_levels':changed_pixels,'snapshots':snapshots,
      'scope':'Functional local-file viewer, transform, texture/material binding, screenshot and offline checks. Not artist acceptance or mechanical certification.'}
    assert hashlib.sha256(args.html.read_bytes()).hexdigest()==html_hash
    (args.output/'verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['snapshots','initial_state','opening_state','closing_state','materials']},indent=2))
    browser.close()
