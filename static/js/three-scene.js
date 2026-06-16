/* ==========================================
   THREE.JS PARTICLE BACKGROUND
========================================== */

let scene;
let camera;
let renderer;
let particles;

let mouseX = 0;
let mouseY = 0;

const PARTICLE_COUNT = 500;

/* ==========================================
   DOM READY
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    if (typeof THREE === "undefined") {
        console.error("Three.js not loaded.");
        return;
    }

    const container = document.getElementById("bg-canvas");

    if (!container) {
        console.warn("#bg-canvas not found.");
        return;
    }

    init(container);
    animate();

});

/* ==========================================
   INIT
========================================== */

function init(container) {

    /* Prevent duplicate canvases */

    container.innerHTML = "";

    /* Scene */

    scene = new THREE.Scene();

    /* Camera */

    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        2000
    );

    camera.position.z = 500;

    /* Renderer */

    renderer = new THREE.WebGLRenderer({
        alpha: true,
        antialias: true
    });

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

    renderer.setPixelRatio(
        Math.min(window.devicePixelRatio, 2)
    );

    renderer.setClearColor(0x000000, 0);

    /* Make sure canvas stays behind content */

    renderer.domElement.style.position = "fixed";
    renderer.domElement.style.top = "0";
    renderer.domElement.style.left = "0";
    renderer.domElement.style.width = "100%";
    renderer.domElement.style.height = "100%";
    renderer.domElement.style.zIndex = "-1";
    renderer.domElement.style.pointerEvents = "none";

    container.appendChild(renderer.domElement);

    /* Geometry */

    const geometry = new THREE.BufferGeometry();

    const positions = new Float32Array(
        PARTICLE_COUNT * 3
    );

    for (let i = 0; i < PARTICLE_COUNT; i++) {

        positions[i * 3] =
            (Math.random() - 0.5) * 1500;

        positions[i * 3 + 1] =
            (Math.random() - 0.5) * 1500;

        positions[i * 3 + 2] =
            (Math.random() - 0.5) * 1500;
    }

    geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(
            positions,
            3
        )
    );

    /* Material */

    const material = new THREE.PointsMaterial({
        color: 0x00d4ff,
        size: 2,
        transparent: true,
        opacity: 0.8
    });

    /* Particles */

    particles = new THREE.Points(
        geometry,
        material
    );

    scene.add(particles);

    /* Light */

    const ambientLight =
        new THREE.AmbientLight(
            0xffffff,
            1
        );

    scene.add(ambientLight);

    /* Events */

    window.addEventListener(
        "resize",
        onResize
    );

    document.addEventListener(
        "mousemove",
        onMouseMove
    );

    console.log(
        "Three.js Particle Background Loaded"
    );
}

/* ==========================================
   MOUSE MOVE
========================================== */

function onMouseMove(event) {

    mouseX =
        (event.clientX -
            window.innerWidth / 2) * 0.001;

    mouseY =
        (event.clientY -
            window.innerHeight / 2) * 0.001;
}

/* ==========================================
   RESIZE
========================================== */

function onResize() {

    if (!camera || !renderer) return;

    camera.aspect =
        window.innerWidth /
        window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
}

/* ==========================================
   ANIMATION LOOP
========================================== */

function animate() {

    requestAnimationFrame(animate);

    if (
        !particles ||
        !renderer ||
        !scene ||
        !camera
    ) {
        return;
    }

    /* Particle Rotation */

    particles.rotation.y += 0.0008;
    particles.rotation.x += 0.0002;

    /* Mouse Interaction */

    camera.position.x +=
        (
            mouseX * 50 -
            camera.position.x
        ) * 0.03;

    camera.position.y +=
        (
            -mouseY * 50 -
            camera.position.y
        ) * 0.03;

    camera.lookAt(scene.position);

    renderer.render(
        scene,
        camera
    );
}