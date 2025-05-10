import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🌲 Урок 3: Герой в 3D гора")

threejs_html = """
<div style="width:100%; height:600px;">
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/examples/js/loaders/GLTFLoader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.150.1/examples/js/controls/OrbitControls.js"></script>
  <canvas id="threeCanvas" width="1000" height="600"></canvas>
  <textarea id="commandInput" rows="4" style="width: 100%; margin-top: 10px;">местя(герой, напред).</textarea>
  <button onclick="runCommands()" style="margin:10px 0;padding:8px 16px;">Изпълни</button>

  <script>
    // Инициализация на сцената
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
    
    // Осветление
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    scene.add(new THREE.AmbientLight(0x404040));

    // Терен
    const groundGeometry = new THREE.PlaneGeometry(50, 50);
    const groundMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x228b22,
      side: THREE.DoubleSide
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Флаг
    const flagGeometry = new THREE.BoxGeometry(0.5, 1, 0.5);
    const flagMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    const flag = new THREE.Mesh(flagGeometry, flagMaterial);
    flag.position.set(5, 0.5, -5);
    flag.castShadow = true;
    scene.add(flag);

    // Герой
    let hero;
    const loader = new THREE.GLTFLoader();
    
    // Зареждане на модела с обработка на грешки
    loader.load(
      'https://raw.githubusercontent.com/MaggieM777/game_3d/main/mini_mario_rigged_mixamo.glb',
      function (gltf) {
        hero = gltf.scene;
        hero.position.set(0, 0, 0);
        hero.scale.set(0.5, 0.5, 0.5);
        
        // Включване на сянка за героя
        hero.traverse(function(node) {
          if (node.isMesh) {
            node.castShadow = true;
          }
        });
        
        scene.add(hero);
        console.log("Моделът е зареден успешно!");
      },
      undefined,
      function (error) {
        console.error("Грешка при зареждане:", error);
        // Създаване на заместител
        const geometry = new THREE.BoxGeometry(1, 2, 1);
        const material = new THREE.MeshStandardMaterial({ color: 0x0000ff });
        hero = new THREE.Mesh(geometry, material);
        hero.position.set(0, 1, 0);
        hero.castShadow = true;
        scene.add(hero);
      }
    );

    // Анимационен цикъл
    function animate() {
      requestAnimationFrame(animate);
      renderer.render(scene, camera);
    }
    animate();

    // Контроли за камерата
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Функция за движение
    function runCommands() {
      const cmds = document.getElementById("commandInput").value
        .split('.')
        .map(c => c.trim())
        .filter(c => c.length > 0);
      
      let index = 0;
      const step = 1.5;

      function executeNext() {
        if (index >= cmds.length) return;
        if (!hero) return;

        const cmd = cmds[index];
        
        if (/местя\\(герой, напред\\)/.test(cmd)) {
          hero.position.z -= step;
        } else if (/местя\\(герой, назад\\)/.test(cmd)) {
          hero.position.z += step;
        } else if (/местя\\(герой, ляво\\)/.test(cmd)) {
          hero.position.x -= step;
        } else if (/местя\\(герой, дясно\\)/.test(cmd)) {
          hero.position.x += step;
        }

        // Проверка за победа
        if (hero.position.distanceTo(flag.position) < 2) {
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
