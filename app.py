import streamlit as st
import streamlit.components.v1 as components
import base64

# Заглавие
st.set_page_config(layout="wide")
st.title("👾 Mario.obj Viewer (Arrow key movement)")

# Зареждаме Mario.obj и го кодираме в base64
with open("Mario.obj", "rb") as f:
    obj_data = f.read()
    obj_base64 = base64.b64encode(obj_data).decode()

# Вграждаме HTML с Three.js
html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Mario Viewer</title>
  <style>body {{ margin: 0; overflow: hidden; }}</style>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.1/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.1/examples/js/loaders/OBJLoader.js"></script>
</head>
<body>
<canvas id="c"></canvas>
<script>
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  const renderer = new THREE.WebGLRenderer({canvas: document.querySelector("#c"), antialias: true});
  renderer.setSize(window.innerWidth, window.innerHeight);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const ambientLight = new THREE.AmbientLight(0xffffff, 1);
  scene.add(ambientLight);

  const loader = new THREE.OBJLoader();
  const objText = atob("{obj_base64}");
  const obj = loader.parse(objText);
  obj.scale.set(0.01, 0.01, 0.01);
  scene.add(obj);

  // Стрелки за движение
  document.addEventListener("keydown", function(event) {{
    switch (event.key) {{
      case "ArrowLeft": obj.position.x -= 0.1; break;
      case "ArrowRight": obj.position.x += 0.1; break;
      case "ArrowUp": obj.position.z -= 0.1; break;
      case "ArrowDown": obj.position.z += 0.1; break;
    }}
  }});

  function animate() {{
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }}

  animate();
</script>
</body>
</html>
"""

components.html(html_content, height=600)
