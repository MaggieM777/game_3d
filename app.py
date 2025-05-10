import streamlit as st
import pathlib

st.set_page_config(page_title="3D Mario Viewer", layout="wide")

st.title("👾 3D Mario Viewer (.obj) with Three.js")

# Път до Mario.obj (в същата директория)
obj_path = pathlib.Path("Mario.obj")
if not obj_path.exists():
    st.error("❌ Файлът Mario.obj не е намерен!")
    st.stop()

# Зареждане на .obj съдържанието като текст
with open(obj_path, "r") as f:
    obj_data = f.read()

# Вграждане на Three.js + JS код
st.components.v1.html(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Mario 3D Model</title>
  <style>
    body {{ margin: 0; overflow: hidden; }}
    canvas {{ display: block; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/three@0.157.0/build/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.157.0/examples/js/loaders/OBJLoader.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.157.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <script>
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xeeeeee);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(0, 1, 1).normalize();
    scene.add(light);

    const objData = `{obj_data.replace("\\", "\\\\").replace("`", "\\`")}`;
    const blob = new Blob([objData], {{type: 'text/plain'}});
    const url = URL.createObjectURL(blob);

    const loader = new THREE.OBJLoader();
    loader.load(url, function (object) {{
      scene.add(object);
    }});

    function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();

    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>
""", height=600)
