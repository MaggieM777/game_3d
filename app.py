import streamlit as st
from streamlit.components.v1 import html

# Заглавие на приложението
st.title("3D модел с .obj във Streamlit")

# Вмъкване на HTML и JavaScript код за зареждане на .obj модел
html_code = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D OBJ Model Viewer</title>
    <style>
      body { margin: 0; overflow: hidden; }
      canvas { display: block; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/OBJLoader2.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/OrbitControls.js"></script>
  </head>
  <body>
    <script>
      var scene = new THREE.Scene();
      var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
      var renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      var controls = new THREE.OrbitControls(camera, renderer.domElement);

      // Създаване на осветление
      var light = new THREE.AmbientLight(0x404040); // soft white light
      scene.add(light);

      // Зареждане на .obj модел
      var loader = new THREE.OBJLoader();
      loader.load(
        'https://threejs.org/examples/models/obj/male02/male02.obj',  // Заменете с пътя към вашия модел
        function (object) {
          scene.add(object);
          object.scale.set(0.1, 0.1, 0.1);  // Променете мащаба на модела
        },
        function (xhr) {
          console.log((xhr.loaded / xhr.total * 100) + '% loaded');
        },
        function (error) {
          console.log('Error loading .obj model', error);
        }
      );

      camera.position.z = 5;

      var animate = function () {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
      };

      animate();
    </script>
  </body>
</html>
"""

# Вмъкване на HTML и JS в Streamlit
html(html_code, height=600)
