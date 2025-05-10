import streamlit as st
import numpy as np
from pythreejs import Scene, PerspectiveCamera, WebGLRenderer, AmbientLight, DirectionalLight, GLTFLoader, Mesh, MeshBasicMaterial, BoxGeometry
from IPython.display import display

# Заглавие на приложението
st.title("3D Model Viewer for Common Frog")

# Въвеждаме път към модела
model_path = "common_frog.glb"

# Проверяваме дали файлът съществува и ако е така, зареждаме модела
try:
    # Създаване на сцена
    scene = Scene()

    # Добавяне на камера
    camera = PerspectiveCamera(fov=75, aspect=1, near=0.1, far=1000, position=[0, 1, 3])
    scene.add(camera)

    # Добавяне на светлини
    scene.add(AmbientLight(intensity=0.5))
    scene.add(DirectionalLight(color='#ffffff', intensity=1, position=[3, 3, 3]))

    # Зареждаме .glb модела с GLTFLoader
    loader = GLTFLoader()
    loader.load(model_path, lambda gltf: scene.add(gltf['scene']))

    # Рендериране на сцената
    renderer = WebGLRenderer()
    renderer.setSize(800, 600)
    renderer.render(scene, camera)

    # Показваме рендерираната сцена в Streamlit
    st.write("Моделът е зареден успешно!")
    st.image(renderer.to_data_url(), use_column_width=True)

except Exception as e:
    st.error(f"Грешка при зареждането на модела: {e}")
