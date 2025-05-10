import streamlit as st
from pythreejs import *
import numpy as np
import os

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

# Задаване на пътя към 3D модела
model_path = 'common_frog.glb'  # Увери се, че пътят е правилен

# Проверка дали моделът е в директорията
if not os.path.exists(model_path):
    st.error(f"Моделът не може да бъде намерен: {model_path}")
else:
    # Зареждане на .glb файл с GLTFLoader
    loader = GLTFLoader()

    def on_load(gltf):
        """Функция, която се извиква след успешното зареждане на модела"""
        scene.add(gltf['scene'])

    # Зареждаме 3D модела и го добавяме към сцената
    loader.load(model_path, on_load)

    # Примерно рендериране
    st.write("Рендерираме 3D модела...")

    # Показваме рендерирането в Streamlit
    st.components.v1.html(renderer)

# Допълнителни Streamlit компоненти за управление на камерата или други взаимодействия
# Може да добавиш бутони или слайдери за интеракция с модела
st.sidebar.title("Контроли")
st.sidebar.write("Може да добавите контроли за взаимодействие с модела тук.")
