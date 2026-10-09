import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const $ = id => document.getElementById(id);
const metadata = JSON.parse($('assetMetadata').textContent);
const viewport = $('viewport');
const errors = [];
let model, mixer, action, clip, angle = 0, playing = false, direction = 1, ready = false;
let openingSeconds = 2, frames = 0, view = 'hero';
let playbackStarted = 0, playbackOffset = 0;
const center = new THREE.Vector3(), size = new THREE.Vector3(), bounds = new THREE.Box3();
const scene = new THREE.Scene();
scene.background = new THREE.Color('#182329');
const camera = new THREE.PerspectiveCamera(35, 1, 0.001, 100);
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1;
renderer.domElement.setAttribute('aria-label', 'Authored car model. Drag to orbit; scroll to zoom.');
renderer.domElement.tabIndex = 0;
viewport.prepend(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.09;
const pmrem = new THREE.PMREMGenerator(renderer);
const room = new RoomEnvironment();
scene.environment = pmrem.fromScene(room, 0.04).texture;
scene.environmentIntensity = 0.75;
room.dispose();
pmrem.dispose();
const hemisphere = new THREE.HemisphereLight(0xe6edf2, 0x4a4842, 1.0);
const key = new THREE.DirectionalLight(0xfff0df, 2.2);
const fill = new THREE.DirectionalLight(0xd8e9ff, 1.0);
scene.add(hemisphere, key, fill, key.target, fill.target);

const lighting = {
  environment: 'Three.js RoomEnvironment, procedural, PMREM blur 0.04', environmentIntensity: 0.75,
  hemisphere: { sky: '#e6edf2', ground: '#4a4842', intensity: 1.0 },
  key: { color: '#fff0df', intensity: 2.2, positionRelativeToModel: [1.5, 2, 2] },
  fill: { color: '#d8e9ff', intensity: 1.0, positionRelativeToModel: [-1, 0.8, -1] },
  toneMapping: 'ACESFilmic', exposure: 1.0, outputColorSpace: 'sRGB',
  materialPolicy: 'GLTFLoader native materials and textures; no material overrides, recoloring, or texture replacements.',
  shadows: false,
};

function render() { renderer.render(scene, camera); }
function resize() {
  const width = Math.max(viewport.clientWidth, 1), height = Math.max(viewport.clientHeight, 1);
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  render();
}
new ResizeObserver(resize).observe(viewport);

function setView(next = 'hero') {
  view = next;
  const vector = ({ hero: [1.0, 0.55, 1.3], side: [0, 0.12, 1], opposite: [0, 0.12, -1] })[view] || [1, 0.55, 1.3];
  const direction = new THREE.Vector3(...vector).normalize();
  const right = new THREE.Vector3().crossVectors(camera.up, direction).normalize();
  const up = new THREE.Vector3().crossVectors(direction, right).normalize();
  const tanY = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)), tanX = tanY * camera.aspect;
  let distance = 0;
  for (const x of [bounds.min.x, bounds.max.x]) for (const y of [bounds.min.y, bounds.max.y]) for (const z of [bounds.min.z, bounds.max.z]) {
    const point = new THREE.Vector3(x, y, z).sub(center);
    distance = Math.max(distance, Math.abs(point.dot(right)) / tanX + point.dot(direction), Math.abs(point.dot(up)) / tanY + point.dot(direction));
  }
  camera.position.copy(center).addScaledVector(direction, distance * 1.23);
  controls.target.copy(center);
  controls.update();
  document.querySelectorAll('[data-view]').forEach(button => button.classList.toggle('active', button.dataset.view === view));
  render();
}

function setAngle(value) {
  if (!Number.isFinite(Number(value))) throw new TypeError('Door angle must be finite');
  angle = THREE.MathUtils.clamp(Number(value), 0, 60);
  if (action) {
    action.enabled = true;
    action.paused = true;
    action.time = angle / 60 * openingSeconds;
    mixer.update(0);
    model.updateMatrixWorld(true);
  }
  $('doorSlider').value = String(angle);
  $('angleValue').textContent = `${Number(angle.toFixed(1))}°`;
  $('doorSlider').setAttribute('aria-valuetext', `${angle.toFixed(1)} degrees open`);
  render();
  return getState();
}

function setPlaying(value) {
  playing = Boolean(value) && Boolean(action) && ready;
  if (angle >= 60) direction = -1;
  if (angle <= 0) direction = 1;
  if (playing) {
    playbackOffset = direction > 0 ? angle / 30 : 4 - angle / 30;
    playbackStarted = performance.now();
  }
  $('playButton').textContent = playing ? 'Pause' : 'Play open / close';
  $('playButton').setAttribute('aria-pressed', String(playing));
  return playing;
}
function reset() { setPlaying(false); direction = 1; setAngle(0); setView('hero'); }
function getTransforms() {
  const result = [];
  if (model) {
    model.updateMatrixWorld(true);
    model.traverse(object => {
      if (!object.isMesh && !object.name.includes('FrontDoor_Control')) return;
      result.push({ name: object.name, isMesh: Boolean(object.isMesh), position: object.position.toArray(),
        quaternion: object.quaternion.toArray(), matrixWorld: object.matrixWorld.toArray() });
    });
  }
  return result;
}
function getState() {
  return { ready, angle, playing, direction, openingSeconds, view, frames, errors: [...errors],
    animation: clip ? { name: clip.name, duration: clip.duration, tracks: clip.tracks.map(t => t.name) } : null,
    cameraPosition: camera.position.toArray(), lighting, metadata };
}
window.assetViewer = { getState, getTransforms, setAngle, setPlaying, setView, reset };
document.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click', () => setView(button.dataset.view)));
$('doorSlider').addEventListener('input', event => { setPlaying(false); setAngle(event.target.value); });
$('playButton').addEventListener('click', () => setPlaying(!playing));
$('resetButton').addEventListener('click', reset);
$('closedButton').addEventListener('click', () => { setPlaying(false); setAngle(0); });
$('openButton').addEventListener('click', () => { setPlaying(false); setAngle(60); });

function materialSummary() {
  const materials = new Map();
  model.traverse(object => {
    if (!object.isMesh) return;
    for (const material of Array.isArray(object.material) ? object.material : [object.material]) {
      if (materials.has(material.uuid)) continue;
      materials.set(material.uuid, { name: material.name, type: material.type,
        baseColorTexture: Boolean(material.map), roughnessTexture: Boolean(material.roughnessMap),
        metallicTexture: Boolean(material.metalnessMap), color: material.color.toArray(),
        metalness: material.metalness, roughness: material.roughness,
        baseColorSpace: material.map?.colorSpace, roughnessColorSpace: material.roughnessMap?.colorSpace });
    }
  });
  return [...materials.values()];
}
window.assetViewer.getMaterials = materialSummary;

async function load() {
  const encoded = $('assetData').textContent.trim();
  const binary = atob(encoded);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  const gltf = await new GLTFLoader().parseAsync(bytes.buffer, '');
  model = gltf.scene;
  scene.add(model);
  model.updateMatrixWorld(true);
  bounds.setFromObject(model, true);
  bounds.getCenter(center); bounds.getSize(size);
  const extent = Math.max(size.x, size.y, size.z);
  camera.near = extent / 1000; camera.far = extent * 100;
  camera.updateProjectionMatrix();
  controls.minDistance = extent * 0.15; controls.maxDistance = extent * 8;
  key.position.copy(center).add(new THREE.Vector3(1.5, 2, 2).multiplyScalar(extent));
  fill.position.copy(center).add(new THREE.Vector3(-1, 0.8, -1).multiplyScalar(extent));
  key.target.position.copy(center); fill.target.position.copy(center);
  clip = gltf.animations.find(animation => animation.tracks.some(track => /FrontDoor_Control/i.test(track.name))) || gltf.animations[0];
  if (clip) {
    mixer = new THREE.AnimationMixer(model);
    action = mixer.clipAction(clip);
    action.play(); action.paused = true;
    openingSeconds = Math.min(2, clip.duration);
  }
  ready = true;
  document.querySelectorAll('[data-motion]').forEach(element => element.disabled = !clip);
  $('animationStatus').textContent = clip ? 'Baked door motion · 2 s open / 2 s close' : 'No animation clip in this asset';
  $('loading').hidden = true;
  resize(); reset();
}

function animate(now) {
  requestAnimationFrame(animate);
  if (playing) {
    const phase = (playbackOffset + (now - playbackStarted) / 1000) % 4;
    direction = phase < 2 ? 1 : -1;
    setAngle(phase < 2 ? phase * 30 : (4 - phase) * 30);
  }
  controls.update(); render(); frames++;
}
requestAnimationFrame(animate);
load().catch(error => {
  errors.push(String(error)); console.error(error);
  $('loading').textContent = `This browser could not open the model: ${error.message || error}`;
  $('loading').classList.add('error');
});
