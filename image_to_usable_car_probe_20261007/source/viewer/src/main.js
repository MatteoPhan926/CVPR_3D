import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const $ = id => document.getElementById(id);
const viewport = $('viewport');
const scene = new THREE.Scene();
scene.background = new THREE.Color('#24363e');
const camera = new THREE.PerspectiveCamera(35, 1, 0.01, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.domElement.setAttribute('aria-label', '3D model; drag to orbit, scroll to zoom');
renderer.domElement.tabIndex = 0;
viewport.prepend(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.075;
controls.maxPolarAngle = Math.PI * 0.49;
const pmrem = new THREE.PMREMGenerator(renderer);
const room = new RoomEnvironment();
const environment = pmrem.fromScene(room, 0.04);
scene.environment = environment.texture;
scene.environmentIntensity = 0.9;
room.dispose();
pmrem.dispose();

const hemisphere = new THREE.HemisphereLight(0xd6e5ef, 0x697a7d, 1.4);
scene.add(hemisphere);
const key = new THREE.DirectionalLight(0xffefdd, 3.2);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.normalBias = 0.025;
key.shadow.bias = -0.00006;
scene.add(key);
scene.add(key.target);
const fill = new THREE.DirectionalLight(0xc7e5ff, 1.2);
scene.add(fill);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.ShadowMaterial({ color: '#070d10', opacity: 0.3 }));
ground.rotation.x = -Math.PI / 2;
ground.receiveShadow = true;
scene.add(ground);

const loader = new GLTFLoader();
const loaded = { raw: null, authored: null };
const urls = { raw: '/raw/car_raw.glb', authored: '/artifacts/car_authored.glb' };
const modelBounds = new THREE.Box3();
const center = new THREE.Vector3();
const span = new THREE.Vector3();
const front = new THREE.Vector3(0, 0, 1);
const side = new THREE.Vector3(1, 0, 0);
let config = {}, mode = 'raw', ready = false, busy = false;
let size = 1, progress = 0, playing = false, playDirection = 1, duration = 2, clipStartTime = 0;
let mixer = null, action = null, pivot = null, pivotClosed = null, hingeAxis = null;
let motionMode = null, motionReason = 'No authored asset loaded', currentView = 'hero';
let maxAngleDegrees = 60, angleSign = 1, frames = 0;
const errors = [];
const warnings = [];
const authoredStatus = { available: null, reason: 'Not checked' };

function notice(error, fatal = false) {
  const message = error instanceof Error ? error.message : String(error);
  (fatal ? errors : warnings).push(message);
  $('loading').hidden = true;
  $('error').hidden = false;
  $('error').textContent = message;
  if (fatal) console.error(error);
}

function validDirection(value, fallback) {
  if (!Array.isArray(value) || value.length !== 3 || !value.every(Number.isFinite)) return fallback.clone();
  const result = new THREE.Vector3(...value);
  if (result.lengthSq() < 1e-12) throw new Error('Configured direction must be nonzero');
  return result.normalize();
}

function prepareModel(gltf, assetMode) {
  gltf.scene.traverse(object => {
    if (!object.isMesh) return;
    object.castShadow = true;
    object.receiveShadow = true;
    // Preserve the loaded GLB's PBR/vertex-color/alpha/material properties.
    for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
      if (material?.map) material.map.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    }
  });
  // Optional explicit presentation rotation; original scene nodes remain intact.
  const rotation = config.display_rotations_degrees?.[assetMode] || [0, 0, 0];
  if (!Array.isArray(rotation) || rotation.length !== 3 || !rotation.every(Number.isFinite)) throw new Error('Display rotation must contain three finite XYZ Euler angles');
  gltf.displayRoot = new THREE.Group();
  gltf.displayRoot.name = `${assetMode}_DisplayRoot`;
  gltf.displayRoot.rotation.set(...rotation.map(THREE.MathUtils.degToRad), 'XYZ');
  gltf.displayRoot.add(gltf.scene);
  gltf.displayRoot.visible = false;
  scene.add(gltf.displayRoot);
  gltf.displayRoot.updateMatrixWorld(true);
  return gltf;
}

function resize() {
  const width = Math.max(1, viewport.clientWidth), height = Math.max(1, viewport.clientHeight);
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function fitStage() {
  modelBounds.makeEmpty();
  for (const asset of Object.values(loaded)) if (asset) modelBounds.union(new THREE.Box3().setFromObject(asset.displayRoot, true));
  if (modelBounds.isEmpty()) throw new Error('The loaded asset has no measurable geometry');
  modelBounds.getCenter(center);
  modelBounds.getSize(span);
  size = Math.max(span.x, span.y, span.z);
  if (!(size > 0) || !Number.isFinite(size)) throw new Error('The loaded asset has invalid bounds');
  // No asset translation, scale normalization, geometry transfer, or inferred hinge.
  ground.position.copy(center).addScaledVector(camera.up, -span.dot(camera.up.clone().set(Math.abs(camera.up.x), Math.abs(camera.up.y), Math.abs(camera.up.z))) / 2 - size * 0.002);
  ground.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), camera.up);
  ground.scale.setScalar(size * 20);
  key.position.copy(center).addScaledVector(side, size * 1.4).addScaledVector(camera.up, size * 2.4).addScaledVector(front, size);
  key.target.position.copy(center);
  key.shadow.camera.left = key.shadow.camera.bottom = -size;
  key.shadow.camera.right = key.shadow.camera.top = size;
  key.shadow.camera.near = size * 0.01;
  key.shadow.camera.far = size * 6;
  key.shadow.normalBias = size * 0.002;
  key.shadow.camera.updateProjectionMatrix();
  fill.position.copy(center).addScaledVector(side, -size).addScaledVector(camera.up, size * 0.8).addScaledVector(front, -size);
  camera.near = size / 1000;
  camera.far = size * 100;
  camera.updateProjectionMatrix();
  controls.minDistance = size * 0.05;
  controls.maxDistance = size * 8;
  scene.fog = new THREE.Fog(scene.background, size * 5, size * 22);
}

function setView(view = 'hero') {
  if (modelBounds.isEmpty()) return;
  currentView = ['hero', 'side', 'front'].includes(view) ? view : 'hero';
  const direction = currentView === 'side' ? side.clone().addScaledVector(camera.up, 0.14)
    : currentView === 'front' ? front.clone().addScaledVector(camera.up, 0.18)
      : side.clone().multiplyScalar(1.38).addScaledVector(camera.up, 0.7).addScaledVector(front, 1.68);
  direction.normalize();
  const right = new THREE.Vector3().crossVectors(camera.up, direction).normalize();
  const up = new THREE.Vector3().crossVectors(direction, right).normalize();
  const tanY = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)), tanX = tanY * camera.aspect;
  let distance = 0;
  for (const x of [modelBounds.min.x, modelBounds.max.x]) for (const y of [modelBounds.min.y, modelBounds.max.y]) for (const z of [modelBounds.min.z, modelBounds.max.z]) {
    const point = new THREE.Vector3(x, y, z).sub(center);
    distance = Math.max(distance, Math.abs(point.dot(right)) / tanX + point.dot(direction), Math.abs(point.dot(up)) / tanY + point.dot(direction));
  }
  camera.position.copy(center).addScaledVector(direction, distance * 1.12);
  controls.target.copy(center);
  controls.update();
  document.querySelectorAll('[data-view]').forEach(button => button.classList.toggle('selected', button.dataset.view === currentView));
  render();
}

function configureMotion() {
  const asset = loaded.authored;
  pivot = asset.scene.getObjectByName(config.door?.pivot_node || 'DoorPivot');
  if (!pivot) { motionReason = 'Authored asset has no configured DoorPivot node'; return; }
  pivotClosed = pivot.quaternion.clone();
  const animationName = config.door?.animation_name;
  const candidateClips = asset.animations.filter(clip => !animationName || clip.name === animationName);
  const clip = candidateClips.length === 1 ? candidateClips[0] : null;
  if (clip && clip.duration > 0) {
    const expectedNames = [pivot.name, pivot.uuid];
    const boundNames = clip.tracks.map(track => THREE.PropertyBinding.parseTrackName(track.name).nodeName);
    if (!clip.tracks.length || !boundNames.every(name => expectedNames.includes(name))) {
      motionReason = 'Selected animation targets nodes outside the authored DoorPivot'; return;
    }
    const openRange = config.door?.clip_open_range_seconds || [0, clip.duration];
    if (!Array.isArray(openRange) || openRange.length !== 2 || !openRange.every(Number.isFinite) || openRange[0] < 0 || openRange[1] > clip.duration + 1e-6 || openRange[1] <= openRange[0]) {
      motionReason = 'Configured clip opening range must be a positive interval inside the animation'; return;
    }
    clipStartTime = openRange[0];
    duration = openRange[1] - openRange[0];
    mixer = new THREE.AnimationMixer(asset.scene);
    action = mixer.clipAction(clip);
    action.setLoop(THREE.LoopOnce, 1);
    action.clampWhenFinished = true;
    action.play();
    action.paused = true;
    action.time = clipStartTime;
    mixer.update(0);
    pivotClosed.copy(pivot.quaternion);
    for (const fraction of [0.5, 1]) {
      action.time = clipStartTime + fraction * duration;
      mixer.update(0);
      const measured = THREE.MathUtils.radToDeg(pivotClosed.angleTo(pivot.quaternion));
      if (Math.abs(measured - maxAngleDegrees * fraction) > 0.01) {
        action.stop();
        pivot.quaternion.copy(pivotClosed);
        motionReason = `Exported pivot angle at ${fraction * 100}% is ${measured.toFixed(3)}°, expected ${maxAngleDegrees * fraction}°`;
        return;
      }
    }
    motionMode = 'exported-animation';
  } else if (Array.isArray(config.door?.axis) && [1, -1].includes(config.door?.sign)) {
    hingeAxis = validDirection(config.door.axis, new THREE.Vector3(0, 1, 0));
    angleSign = config.door.sign;
    motionMode = 'configured-local-pivot';
  } else {
    motionReason = 'A single DoorPivot animation or an explicit local hinge axis and sign is required'; return;
  }
  motionReason = null;
  setProgress(0);
}

function setPlaying(value) {
  playing = Boolean(value) && mode === 'authored' && Boolean(motionMode) && ready;
  if (progress >= 1) playDirection = -1;
  if (progress <= 0) playDirection = 1;
  $('playIcon').textContent = playing ? 'Ⅱ' : '\u25b6\ufe0e';
  $('playLabel').textContent = playing ? 'Pause motion' : 'Play motion';
  return playing;
}

function updateLabels() {
  const angle = progress * maxAngleDegrees;
  $('angleValue').innerHTML = `${Number(angle.toFixed(1))}° <span>/ ${maxAngleDegrees}°</span>`;
  $('percentValue').textContent = `${Math.round(progress * 100)}%`;
  $('doorSlider').value = String(angle);
  $('doorSlider').style.setProperty('--pct', `${progress * 100}%`);
  $('doorSlider').setAttribute('aria-valuetext', `${Number(angle.toFixed(1))} degrees open`);
  const isRaw = mode === 'raw';
  $('modeBadge').textContent = isRaw ? 'Raw generation' : 'Authored asset';
  $('originalButton').textContent = isRaw ? 'View authored' : 'Compare raw';
  $('originalButton').setAttribute('aria-pressed', String(isRaw));
  $('controlEyebrow').textContent = isRaw ? 'RAW GENERATION' : motionMode ? 'AUTHORED DOOR MOTION' : 'AUTHORED ASSET';
  $('controlHeading').textContent = isRaw ? 'Static raw asset' : motionMode ? 'Visible cabin door' : 'Motion unavailable';
  $('downloadLink').href = urls[mode];
  document.body.classList.toggle('original', isRaw);
  for (const id of ['doorSlider', 'playButton', 'closedButton', 'openButton']) $(id).disabled = isRaw || !motionMode;
}

function setProgress(value) {
  const next = Number(value);
  if (!Number.isFinite(next)) throw new TypeError('Progress must be finite');
  progress = THREE.MathUtils.clamp(next, 0, 1);
  if (motionMode === 'exported-animation') {
    action.enabled = true;
    action.paused = true;
    action.time = clipStartTime + progress * duration;
    mixer.update(0);
  } else if (motionMode === 'configured-local-pivot') {
    pivot.quaternion.copy(pivotClosed).multiply(new THREE.Quaternion().setFromAxisAngle(hingeAxis, angleSign * THREE.MathUtils.degToRad(progress * maxAngleDegrees)));
  }
  loaded.authored?.scene.updateMatrixWorld(true);
  updateLabels();
  render();
  return getState();
}

async function setMode(value) {
  if (!['raw', 'authored'].includes(value)) throw new Error('Mode must be raw or authored');
  if (busy) return getState();
  setPlaying(false);
  if (!loaded[value]) {
    busy = true;
    $('loadingText').textContent = `Opening ${value} GLB…`;
    $('loading').hidden = false;
    try {
      loaded[value] = prepareModel(await loader.loadAsync(urls[value]), value);
      if (value === 'authored') {
        authoredStatus.available = true;
        authoredStatus.reason = null;
        configureMotion();
      }
      fitStage();
    } catch (error) {
      if (value === 'authored') {
        authoredStatus.available = false;
        authoredStatus.reason = String(error);
      }
      notice(`${value} GLB is unavailable at ${urls[value]}. ${String(error)}`);
      throw error;
    } finally { busy = false; $('loading').hidden = true; }
  }
  mode = value;
  for (const [name, asset] of Object.entries(loaded)) if (asset) asset.displayRoot.visible = name === mode;
  $('error').hidden = true;
  updateLabels();
  render();
  return getState();
}

function getTransforms(selectedMode = mode) {
  const nodes = [];
  loaded[selectedMode]?.scene.updateMatrixWorld(true);
  loaded[selectedMode]?.scene.traverse(object => {
    if (object.isMesh || object === pivot) nodes.push({
      name: object.name, uuid: object.uuid, type: object.type,
      position: object.getWorldPosition(new THREE.Vector3()).toArray(),
      quaternion: object.getWorldQuaternion(new THREE.Quaternion()).toArray(),
      matrixWorld: object.matrixWorld.toArray()
    });
  });
  return nodes;
}

function getMaterials(selectedMode = mode) {
  const result = [];
  loaded[selectedMode]?.scene.traverse(object => {
    if (!object.isMesh) return;
    for (const material of Array.isArray(object.material) ? object.material : [object.material]) result.push({
      mesh: object.name, name: material.name, type: material.type, color: material.color?.getHexString(),
      vertexColors: material.vertexColors, geometryColorAttribute: Boolean(object.geometry.attributes.color),
      flatShading: material.flatShading,
      metalness: material.metalness, roughness: material.roughness, transparent: material.transparent,
      opacity: material.opacity, alphaTest: material.alphaTest, side: material.side,
      textures: ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap', 'emissiveMap', 'alphaMap'].filter(key => material[key])
    });
  });
  return result;
}

function getState() {
  return {
    ready, mode, original: mode === 'raw', progress, angleDegrees: progress * maxAngleDegrees,
    maxAngleDegrees, playing, motionMode, motionReason, authoredStatus: { ...authoredStatus },
    measuredPivotAngleDegrees: pivot && pivotClosed ? THREE.MathUtils.radToDeg(pivotClosed.angleTo(pivot.quaternion)) : null,
    animationDuration: duration, clipOpeningRangeSeconds: [clipStartTime, clipStartTime + duration], animations: loaded.authored?.animations.map(clip => ({ name: clip.name, duration: clip.duration, tracks: clip.tracks.map(track => track.name) })) || [],
    urls: { ...urls }, cameraView: currentView, cameraPosition: camera.position.toArray(), cameraTarget: controls.target.toArray(),
    cameraBasis: { front: front.toArray(), side: side.toArray(), up: camera.up.toArray() },
    displayRotationsDegrees: { raw: config.display_rotations_degrees?.raw || [0, 0, 0], authored: config.display_rotations_degrees?.authored || [0, 0, 0] },
    bounds: { min: modelBounds.min.toArray(), max: modelBounds.max.toArray() }, frames,
    renderer: { threeRevision: THREE.REVISION, width: renderer.domElement.width, height: renderer.domElement.height },
    errors: [...errors], warnings: [...warnings]
  };
}

function render() { renderer.render(scene, camera); frames += 1; }

window.authoringAPI = {
  get ready() { return ready; }, setProgress,
  setAngle(degrees) { return setProgress(Number(degrees) / maxAngleDegrees); },
  setMode, setOriginal(value) { return setMode(value ? 'raw' : 'authored'); },
  setPlaying, setView, getState, getTransforms, getMaterials,
  screenshot() { render(); return renderer.domElement.toDataURL('image/png'); }
};
$('doorSlider').addEventListener('input', event => { setPlaying(false); setProgress(Number(event.target.value) / maxAngleDegrees); });
$('playButton').addEventListener('click', () => setPlaying(!playing));
$('closedButton').addEventListener('click', () => { setPlaying(false); setProgress(0); });
$('openButton').addEventListener('click', () => { setPlaying(false); setProgress(1); });
$('originalButton').addEventListener('click', () => setMode(mode === 'raw' ? 'authored' : 'raw').catch(() => {}));
$('resetCamera').addEventListener('click', () => setView('hero'));
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => setView(button.dataset.view)));
new ResizeObserver(resize).observe(viewport);
resize();

async function main() {
  config = await fetch('./config.json').then(response => { if (!response.ok) throw new Error('Viewer config.json is missing'); return response.json(); });
  const authoringConfig = await fetch('/artifacts/authoring_config.json').then(response => response.ok ? response.json() : {}).catch(() => ({}));
  config = { ...config, ...authoringConfig, camera: { ...config.camera, ...authoringConfig.camera }, door: { ...config.door, ...authoringConfig.door }, display_rotations_degrees: { ...config.display_rotations_degrees, ...authoringConfig.display_rotations_degrees } };
  urls.raw = config.raw_url || urls.raw;
  urls.authored = config.authored_url || urls.authored;
  maxAngleDegrees = Number(config.door?.max_angle_degrees ?? 60);
  if (maxAngleDegrees !== 60) throw new Error('This probe declares a 0–60 degree opening range; config must match');
  const axisVectors = { X: [1, 0, 0], Y: [0, 1, 0], Z: [0, 0, 1], '-X': [-1, 0, 0], '-Y': [0, -1, 0], '-Z': [0, 0, -1] };
  const upAxis = config.camera?.up_axis ?? config.up_axis;
  if (upAxis && !axisVectors[upAxis]) throw new Error('up_axis must be X, Y, Z, -X, -Y, or -Z');
  camera.up.copy(validDirection(upAxis ? axisVectors[upAxis] : config.camera?.up, new THREE.Vector3(0, 1, 0)));
  front.copy(validDirection(config.camera?.front, new THREE.Vector3(0, 0, 1)));
  side.copy(validDirection(config.camera?.side, new THREE.Vector3(1, 0, 0)));
  if (config.door?.side === '-X' || config.door?.side === 'negative_x' || config.door?.side === -1) side.set(-1, 0, 0);
  if (Math.abs(front.dot(camera.up)) > 0.999 || Math.abs(side.dot(camera.up)) > 0.999) throw new Error('Front and side camera directions must differ from up');
  $('loadingText').textContent = 'Loading the raw generated car…';
  loaded.raw = prepareModel(await loader.loadAsync(urls.raw), 'raw');
  loaded.raw.displayRoot.visible = true;
  fitStage();
  setView('hero');
  ready = true;
  $('loading').hidden = true;
  updateLabels();
}

let last = performance.now();
function tick(now) {
  requestAnimationFrame(tick);
  const delta = Math.min((now - last) / 1000, 0.1);
  last = now;
  if (playing) {
    let next = progress + (delta / duration) * playDirection;
    if (next >= 1) { next = 1; playDirection = -1; }
    if (next <= 0) { next = 0; playDirection = 1; }
    setProgress(next);
  }
  controls.update();
  render();
}
updateLabels();
requestAnimationFrame(tick);
main().catch(error => notice(`Raw GLB could not be opened. ${String(error)}`, true));
