import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🌲 Урок 3: Герой в 3D гора")

threejs_html = """
<div style="width:100%; height:600px;">
  <script type="module">
    // Use exact CDN URLs for all Three.js modules
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';
    import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/GLTFLoader.js';
    import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/controls/OrbitControls.js';

    const canvas = document.getElementById("threeCanvas");
    const renderer = new THREE.WebGLRenderer({ 
      canvas: canvas, 
      antialias: true,
      alpha: true
    });
    renderer.setSize(canvas.width, canvas.height);
    renderer.shadowMap.enabled = true;
    
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa8dadc);

    const camera = new THREE.PerspectiveCamera(60, canvas.width / canvas.height, 0.1, 1000);
    camera.position.set(0, 5, 10);
    camera.lookAt(0, 0, 0);
    
    // Lighting
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    scene.add(new THREE.AmbientLight(0x404040));

    // Ground
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(50, 50),
      new THREE.MeshStandardMaterial({ 
        color: 0x228b22,
        side: THREE.DoubleSide
      })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Flag
    const flag = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 1, 0.5),
      new THREE.MeshStandardMaterial({ color: 0xff0000 })
    );
    flag.position.set(5, 0.5, -5);
    flag.castShadow = true;
    scene.add(flag);

    // Hero character
    let hero;
    const loader = new GLTFLoader();
    
    // Load model with error handling
    loader.load(
      'https://raw.githubusercontent.com/MaggieM777/game_3d/main/mini_mario_rigged_mixamo.glb',
      (gltf) => {
        hero = gltf.scene;
        hero.position.set(0, 0, 0);
        hero.scale.set(0.5, 0.5, 0.5);
        
        // Enable shadows for all parts
        hero.traverse((node) => {
          if (node.isMesh) {
            node.castShadow = true;
          }
        });
        
        scene.add(hero);
        console.log("Model loaded successfully!");
      },
      undefined,
      (error) => {
        console.error("Error loading model:", error);
        // Fallback cube
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const material = new THREE.MeshStandardMaterial({ color: 0x0000ff });
        hero = new THREE.Mesh(geometry, material);
        hero.position.set(0, 1, 0);
        scene.add(hero);
      }
    );

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }
    animate();

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Movement function - must be attached to window
    window.runCommands = function() {
      const cmds = document.getElementById("commandInput").value
        .split('.')
        .map(c => c.trim())
        .filter(c => c.length > 0);
      
      let index = 0;
      const step = 1.5;

      function executeNext() {
        if (index >= cmds.length || !hero) return;

        const cmd = cmds[index];
        
        if (/местя\(герой, напред\)/.test(cmd)) {
          hero.position.z -= step;
        } else if (/местя\(герой, назад\)/.test(cmd)) {
          hero.position.z += step;
        } else if (/местя\(герой, ляво\)/.test(cmd)) {
          hero.position.x -= step;
        } else if (/местя\(герой, дясно\)/.test(cmd)) {
          hero.position.x += step;
        }

        // Check if reached flag
        if (hero.position.distanceTo(flag.position) < 2) {
          alert("🎉 Поздравления! Достигна целта!");
        }

        index++;
        setTimeout(executeNext, 700);
      }

      executeNext();
    };
  </script>

  <canvas id="threeCanvas" width="1000" height="600"></canvas>
  <textarea id="commandInput" rows="4" style="width: 100%; margin-top: 10px;">местя(герой, напред).</textarea>
  <button onclick="runCommands()" style="margin:10px 0;padding:8px 16px;">Изпълни</button>
</div>
"""

components.html(threejs_html, height=700)
