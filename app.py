import streamlit as st
from pathlib import Path
import requests

def download_obj_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def main():
    st.title("Управление на герой с клавиатурни стрелки")
    
    obj_url = "https://threejs.org/examples/models/obj/male02/male02.obj"
    obj_path = "male02.obj"
    
    if not Path(obj_path).exists():
        download_obj_file(obj_url, obj_path)
    
    # HTML + JavaScript код с клавиатурно управление
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Three.js Управление със стрелки</title>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/loaders/OBJLoader.js"></script>
        <style>
            body {{ margin: 0; }}
            canvas {{ display: block; width: 100%; height: 100vh; }}
        </style>
    </head>
    <body>
        <script>
            // Инициализация
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xf0f0f0);
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Осветление
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(1, 1, 1);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040));

            // Зареждане на модела
            const loader = new THREE.OBJLoader();
            let hero;
            loader.load(
                "{obj_url}",
                function (object) {{
                    hero = object;
                    scene.add(hero);
                    hero.position.set(0, 0, 0);  // Начална позиция
                    hero.scale.set(0.5, 0.5, 0.5);  // Мащабиране (ако е твърде голям)
                }},
                undefined,
                function (error) {{
                    console.error("Грешка при зареждане:", error);
                }}
            );

            // Настройки за движение
            const moveSpeed = 0.2;
            const keys = {{ ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false }};

            // Следи натискане на клавиши
            window.addEventListener('keydown', (event) => {{
                if (keys.hasOwnProperty(event.code)) {{
                    keys[event.code] = true;
                }}
            }});
            window.addEventListener('keyup', (event) => {{
                if (keys.hasOwnProperty(event.code)) {{
                    keys[event.code] = false;
                }}
            }});

            // Анимация и движение
            function animate() {{
                requestAnimationFrame(animate);
                
                if (hero) {{
                    // Управление със стрелки
                    if (keys.ArrowUp) hero.position.z -= moveSpeed;    // Напред
                    if (keys.ArrowDown) hero.position.z += moveSpeed;  // Назад
                    if (keys.ArrowLeft) hero.position.x -= moveSpeed;  // Вляво
                    if (keys.ArrowRight) hero.position.x += moveSpeed; // Вдясно
                    
                    // Въртене (опционално)
                    if (keys.ArrowLeft || keys.ArrowRight) {{
                        hero.rotation.y = keys.ArrowLeft ? Math.PI/4 : -Math.PI/4;
                    }} else {{
                        hero.rotation.y = 0;
                    }}
                }}
                
                renderer.render(scene, camera);
            }}
            
            camera.position.set(0, 5, 10);  // Позиция на камерата (поглед отгоре)
            camera.lookAt(0, 0, 0);
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
    st.markdown("**Инструкции:** Използвайте стрелките на клавиатурата (↑, ↓, ←, →) за движение.")

if __name__ == "__main__":
    main()
