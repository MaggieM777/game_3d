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

🚩 Целта е да достигнеш червеното знаме.
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
    camera.lookAt(0, 0, 0);
    
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    // Terrain (Гора)
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(50, 50),
      new THREE.MeshStandardMaterial({ color: 0x228b22 })
    );
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // Flag (целева точка)
    const flag = new THREE.Mesh(
      new THREE.BoxGeometry(0.5, 1, 0.5),
      new THREE.MeshStandardMaterial({ color: 0xff0000 })
    );
    flag.position.set(5, 0.5, -5);
    scene.add(flag);

    // Герой
    let hero;
    const loader = new THREE.GLTFLoader();
    
    // Публичен URL към модела от GitHub
    const modelUrl = "https://raw.githubusercontent.com/MaggieM777/game_3d/main/mini_mario_rigged_mixamo.glb";
    
    loader.load(
      modelUrl,
      function (gltf) {
        hero = gltf.scene;
        hero.position.set(0, 0, 0);
        hero.scale.set(0.5, 0.5, 0.5); // Регулиране размера
        scene.add(hero);
        animate();
      },
      undefined,
      function (error) {
        console.error("Грешка при зареждане на модела:", error);
        // Създаване на временен куб ако модела не се зареди
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const material = new THREE.MeshStandardMaterial({ color: 0x0000ff });
        hero = new THREE.Mesh(geometry, material);
        hero.position.set(0, 1, 0);
        scene.add(hero);
        animate();
      }
    );

    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }

    // Изпълнение на командите
    function runCommands() {
      const cmds = document.getElementById("commandInput").value
        .split('.')
        .map(c => c.trim())
        .filter(c => c.length > 0);
      let index = 0;

      function executeNext() {
        if (index >= cmds.length) return;

        let cmd = cmds[index];
        const step = 1;

        if (!hero) return;

        if (/местя\\(герой, напред\\)/.test(cmd)) {
          hero.position.z -= step;
        } else if (/местя\\(герой, назад\\)/.test(cmd)) {
          hero.position.z += step;
        } else if (/местя\\(герой, ляво\\)/.test(cmd)) {
          hero.position.x -= step;
        } else if (/местя\\(герой, дясно\\)/.test(cmd)) {
          hero.position.x += step;
        }

        // Проверка дали героят е достигнал целта
        const dx = hero.position.x - flag.position.x;
        const dz = hero.position.z - flag.position.z;
        if (Math.sqrt(dx*dx + dz*dz) < 1.5) {
          alert("🎉 Поздравления! Достигна целта!");
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
