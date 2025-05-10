import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🌲 Урок 3: Герой в 3D гора")

st.markdown("""
## 🎮 Инструкции

В този урок ще управляваш анимиран герой в 3D среда чрез команди, подобни на тези в Prolog:

- `местя(герой, напред).`
- `местя(герой, назад).`
- `местя(герой, ляво).`
- `местя(герой, дясно).`

🚩 Целта е да достигнеш червеното знаме, избягвайки препятствия.
""")

threejs_html = """
<div style="width:100%; height:600px;">
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/examples/js/loaders/GLTFLoader.js"></script>
  <canvas id="threeCanvas" width="1000" height="600"></canvas>
  <textarea id="commandInput" rows="4" style="width: 100%; margin-top: 10px;">местя(герой, напред).</textarea>
  <button onclick="runCommands()" style="margin:10px 0;padding:8px 16px;">Изпълни</button>

  <script>
    const canvas = document.getElementById("threeCanvas");
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(canvas.width, canvas.height);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa8dadc);

    const camera = new THREE.PerspectiveCamera(60, canvas.width / canvas.height, 0.1, 1000);
    camera.position.set(0, 5, 10);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(50, 50),
      new THREE.MeshStandardMaterial({ color: 0x228b22 })
    );
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // Flag (goal)
    const flag = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 1, 0.5),
      new THREE.MeshStandardMaterial({ color: 0xff0000 })
    );
    flag.position.set(5, 0.5, -5);
    scene.add(flag);

    // Obstacles
    const obstacles = [];
    function addObstacle(x, z) {
      const obs = new THREE.Mesh(
        new THREE.BoxGeometry(1, 1, 1),
        new THREE.MeshStandardMaterial({ color: 0x555555 })
      );
      obs.position.set(x, 0.5, z);
      scene.add(obs);
      obstacles.push(obs);
    }

    addObstacle(2, -1);
    addObstacle(3, -3);
    addObstacle(1, -4);

    // Trees
    function addTree(x, z) {
      const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.2, 0.2, 1),
        new THREE.MeshStandardMaterial({ color: 0x8b4513 })
      );
      trunk.position.set(x, 0.5, z);

      const crown = new THREE.Mesh(
        new THREE.SphereGeometry(0.5),
        new THREE.MeshStandardMaterial({ color: 0x006400 })
      );
      crown.position.set(x, 1.3, z);

      scene.add(trunk);
      scene.add(crown);
    }

    addTree(2, 2);
    addTree(-2, -3);
    addTree(-4, 4);

    // Hero
    let hero, mixer, animations;
    const loader = new THREE.GLTFLoader();
    loader.load("/mini_mario_rigged_mixamo.glb", function (gltf) {
      hero = gltf.scene;
      hero.position.set(0, 0, 0);
      hero.scale.set(1.2, 1.2, 1.2);
      scene.add(hero);

      mixer = new THREE.AnimationMixer(hero);
      if (gltf.animations.length > 0) {
        const action = mixer.clipAction(gltf.animations[0]);
        action.play();
      }

      animate();
    });

    const clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      if (mixer) mixer.update(clock.getDelta());
      renderer.render(scene, camera);
    }

    function isBlocked(x, z) {
      for (const obs of obstacles) {
        const dx = obs.position.x - x;
        const dz = obs.position.z - z;
        if (Math.sqrt(dx*dx + dz*dz) < 1) return true;
      }
      return false;
    }

    function runCommands() {
      const cmds = document.getElementById("commandInput").value
        .split('.')
        .map(c => c.trim())
        .filter(c => c.length > 0);
      let index = 0;

      function executeNext() {
        if (index >= cmds.length || !hero) return;

        const step = 1;
        let cmd = cmds[index];
        let newX = hero.position.x;
        let newZ = hero.position.z;

        if (/местя\\(герой, напред\\)/.test(cmd)) newZ -= step;
        else if (/местя\\(герой, назад\\)/.test(cmd)) newZ += step;
        else if (/местя\\(герой, ляво\\)/.test(cmd)) newX -= step;
        else if (/местя\\(герой, дясно\\)/.test(cmd)) newX += step;

        if (!isBlocked(newX, newZ)) {
          hero.position.x = newX;
          hero.position.z = newZ;
        }

        const dx = hero.position.x - flag.position.x;
        const dz = hero.position.z - flag.position.z;
        if (Math.sqrt(dx*dx + dz*dz) < 1) {
          alert("🎉 Поздравления! Достигна целта!");
          const audio = new Audio("https://www.soundjay.com/buttons/sounds/button-3.mp3");
          audio.play();
        }

        index++;
        setTimeout(executeNext, 700);
      }

      executeNext();
    }
  </script>
</div>
"""

components.html(threejs_html, height=700)
