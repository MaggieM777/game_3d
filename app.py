import streamlit as st
from pathlib import Path
import requests

# Функция за изтегляне на .obj файла (ако не е локален)
def download_obj_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Streamlit app
def main():
    st.title("3D модел на герой с Three.js в Streamlit")
    
    # URL на .obj файла
    
    
    # Ако искате да го кеширате локално
    obj_path = "Mario.obj"
    
    if not Path(obj_path).exists():
        download_obj_file(obj_url, obj_path)
    
    # Three.js визуализация чрез HTML
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Three.js 3D Model</title>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/loaders/OBJLoader.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/controls/OrbitControls.js"></script>
        <style>
            body {{ margin: 0; }}
            canvas {{ display: block; width: 100%; height: 100vh; }}
        </style>
    </head>
    <body>
        <script>
            // Инициализация на сцена, камера и рендер
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf0f0f0);
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Добавяне на контроли за орбита
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            camera.position.set(5, 5, 5);
            controls.update();

            // Осветление
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(1, 1, 1);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040));

            // Зареждане на .obj модела
            const loader = new THREE.OBJLoader();
            loader.load(
                "{obj_url}",  // или "./male02.obj" ако сте го запазили
                function (object) {{
                    scene.add(object);
                }},
                function (xhr) {{
                    console.log((xhr.loaded / xhr.total * 100) + '% зареден');
                }},
                function (error) {{
                    console.error('Грешка при зареждане на модела:', error);
                }}
            );

            // Анимация
            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}
            animate();

            // Респонсивност
            window.addEventListener('resize', () => {{
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }});
        </script>
    </body>
    </html>
    """
    
    st.components.v1.html(html_code, height=600)

if __name__ == "__main__":
    main()
