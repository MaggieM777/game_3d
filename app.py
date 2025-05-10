import streamlit as st
import pythreejs
from pythreejs import *
import numpy as np

# Създаване на Streamlit интерфейс
st.title("3D Модел с Three.js в Streamlit")

# Зареждане на 3D модел
st.write("Зареждаме .glb модел...")

# Създаване на сцена
scene = Scene()

# Камера
camera = PerspectiveCamera(fov=75, aspect=1, near=0.1, far=1000)
camera.position = [0, 1, 5]

# Добавяне на светлина
light = DirectionalLight(color='white', intensity=1)
light.position = [0, 1, 1]
scene.add(light)

# Рендерър
renderer = WebGLRenderer(width=800, height=600)
renderer.scene = scene
renderer.camera = camera

# Зареждане на .glb файл
loader = GLTFLoader()
loader.load('common_frog.glb', lambda gltf: scene.add(gltf['scene']))

# Примерно рендериране
st.write("Рендерираме модела...")

# Показваме рендерирането в Streamlit
st.components.v1.html(renderer)
