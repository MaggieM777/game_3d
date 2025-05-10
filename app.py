import streamlit as st
import pyrender
import trimesh
import numpy as np

# Заглавие на приложението
st.title("3D Model Viewer with Streamlit")

# В този пример, задаваме фиксиран път към .glb модел
model_path = "common_frog.glb"  # Заменете с пътя към вашия .glb файл

# Проверяваме дали пътят към модела съществува
if model_path:
    try:
        # Зареждаме модела с помощта на Trimesh
        mesh = trimesh.load(model_path)

        # Преобразуваме модела в Pyrender Scene
        scene = pyrender.Scene()

        # Създаваме рендер камера
        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)

        # Създаваме светлина
        light = pyrender.PointLight(color=np.ones(3), intensity=10.0)

        # Добавяме камерата и светлината към сцената
        scene.add(camera, pose=np.eye(4))
        scene.add(light, pose=np.eye(4))

        # Преобразуваме Trimesh модела в Pyrender
        mesh = pyrender.Mesh.from_trimesh(mesh)

        # Добавяме мрежата към сцената
        scene.add(mesh)

        # Настройване на изгледа и рендериране на сцена
        renderer = pyrender.OffscreenRenderer(800, 600)
        color, depth = renderer.render(scene)

        # Показваме изображението в Streamlit
        st.image(color)

    except Exception as e:
        st.error(f"Грешка при зареждането на модела: {e}")
else:
    st.info("Моля, въведете път към .glb модел.")
