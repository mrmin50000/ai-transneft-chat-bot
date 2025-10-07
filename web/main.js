import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

let modelClips = {
    greeting: { name: '03_Sphere_bot_Open', action: null },
    idle: { name: '01_Sphere_bot_Roll', action: null },
    response: { name: '02_Sphere_bot_Run_Cycle', action: null },
}

function onModelLoad(gltf) {
    const model = gltf.scene;
    scene.add(model);
    const clips = gltf.animations;
    mixer = new THREE.AnimationMixer(model);

    greetingClip = THREE.AnimationClip.findByName(clips, modelClips.greeting.name)
    const greetingAction = mixer.clipAction(greetingClip);
    greetingAction.loop = THREE.LoopOnce;
    modelClips.greeting.action = greetingAction;

    idleClip = THREE.AnimationClip.findByName(clips, modelClips.idle.name)
    const idleAction = mixer.clipAction(idleClip);
    idleAction.loop = THREE.LoopOnce;
    modelClips.idle.action = idleAction;

    responseClip = THREE.AnimationClip.findByName(clips, modelClips.response.name)
    const responseAction = mixer.clipAction(responseClip);
    responseAction.loop = THREE.LoopOnce;
    modelClips.response.action = responseAction;

    // mixer.addEventListener('finished', (e) => {
    //     if (e.action.getClip().name === '01_Sphere_bot_Roll') {
    //         runAction.reset();
    //         runAction.play();
    //     }
    // })
}

const scene = new THREE.Scene();

let mixer;
let idleClip;
let responseClip;
let greetingClip;
await loader.loadAsync('./assets/sphere_bot.glb', undefined)
    .then(onModelLoad)
    .catch((error) => console.error(error));

const renderer = new THREE.WebGLRenderer({ antialias: true });
const container = document.querySelector("#character-renderer")
renderer.setSize(container.clientWidth - 16, container.clientHeight - 16);
container.appendChild(renderer.domElement)

const light = new THREE.AmbientLight(0xffffff);
scene.add(light);

const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.set(2, 0.75, 2);
camera.lookAt(0, 0.75, 0);

const clock = new THREE.Clock();
function animate() {
    mixer.update(clock.getDelta());
    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);

function resetAllActions() {
    for (const [_, value] of Object.entries(modelClips)) {
        value.action.stop();
        // value.action.reset();
    }
}

const greetBtn = document.querySelector("#greet")
greetBtn.addEventListener('click', (e) => {
    resetAllActions();
    modelClips.greeting.action.play();
})
const idleBtn = document.querySelector("#idle")
idleBtn.addEventListener('click', (e) => {
    resetAllActions();
    modelClips.idle.action.play();
})
const responseBtn = document.querySelector("#response")
responseBtn.addEventListener('click', (e) => {
    resetAllActions();
    modelClips.response.action.play();
})


