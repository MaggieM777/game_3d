import streamlit as st
import numpy as np
import os

# Импортиране на необходимите библиотеки за визуализация на 3D модел с Three.js
from streamlit.components.v1 import html

# HTML + JavaScript код за зареждане на онлайн 3D модел
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Model Viewer</title>
    <style>
        body { margin: 0; overflow: hidden; }
        canvas { display: block; }
    </style>
</head>
<body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/loaders/OBJLoader.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js"></script>

    <script>
        // Създаване на сцена и камера
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Зареждаме 3D модела от онлайн URL
        var loader = new THREE.OBJLoader();
        loader.load('https://threejs.org/examples/models/obj/male02/male02.obj', function (object) {
            object.scale.set(0.1, 0.1, 0.1);  // Променяме мащаба на модела
            scene.add(object);
        });

        // Добавяне на светлина
        var light = new THREE.AmbientLight(0x404040); // Мека бяла светлина
        scene.add(light);

        // Позиционираме камерата
        camera.position.z = 5;

        // Контроли за движение на камерата
        var controls = new THREE.OrbitControls(camera, renderer.domElement);

        // Функция за анимация на сцената
        function animate() {
            requestAnimationFrame(animate);
            controls.update();  // Извършваме обновление на контролните действия
            renderer.render(scene, camera);  // Рендерираме сцената
        }

        animate();
    </script>
</body>
</html>
"""

# Използваме Streamlit за да вградим HTML/JavaScript код в приложението
st.components.v1.html(html_code, height=800)

