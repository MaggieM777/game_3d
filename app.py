import streamlit as st
import pyrender
import trimesh
import numpy as np

# Зареждаме 3D модела (.glb файл) с trimesh
model_path = 'common_frog.glb'  # Увери се, че пътят е правилен

if not os.path.exists(model_path):
    st.error(f"Моделът не може да бъде намерен: {model_path}")
else:
    # Зареждаме модела с trimesh
    mesh = trimesh.load(model_path)
    
    # Създаваме рендеринг на сцената с pyrender
    scene = pyrender.Scene()
    mesh_node = pyrender.Node(mesh=mesh)
    scene.add_node(mesh_node)

    # Камера
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    camera_node = pyrender.Node(camera=camera, translation=[0, 0, 5])
    scene.add_node(camera_node)

    # Светлина
    light = pyrender.DirectionalLight(color=np.ones(3), intensity=3.0)
    light_node = pyrender.Node(light=light, translation=[0, 10, 10])
    scene.add_node(light_node)

    # Рендерираме сцената
    viewer = pyrender.Viewer(scene, use_raymond_lighting=True)

    # Добавяме рендериране в Streamlit
    st.write("Рендерираме 3D модела...")
    st.pyplot(viewer)
