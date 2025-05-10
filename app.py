import streamlit as st

def main():
    st.title("Управление на герой със стрелки")
    
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Three.js Управление</title>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/examples/js/loaders/OBJLoader.js"></script>
        <style>
            body { margin: 0; overflow: hidden; }
            canvas { display: block; }
        </style>
    </head>
    <body>
        <script>
            // Инициализация
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // Осветление
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(1, 1, 1);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040));

            // Герой
            let hero;
            const loader = new THREE.OBJLoader();
            loader.load(
                'https://threejs.org/examples/models/obj/male02/male02.obj',
                (object) => {
                    hero = object;
                    scene.add(hero);
                    hero.position.set(0, 0, 0);
                    hero.scale.set(0.5, 0.5, 0.5);
                }
            );

            // Камера
            camera.position.set(0, 3, 5);
            camera.lookAt(0, 0, 0);

            // Управление
            const keys = {};
            const moveSpeed = 0.1;
            
            // Фокусиране на iframe-а при клик
            document.addEventListener('click', () => {
                window.focus();
            });

            // Следи натискане на клавиши
            window.addEventListener('keydown', (e) => {
                keys[e.code] = true;
                e.preventDefault(); // Спира скрола на страницата
            });
            
            window.addEventListener('keyup', (e) => {
                keys[e.code] = false;
            });

            // Анимация
            function animate() {
                requestAnimationFrame(animate);
                
                if (hero) {
                    if (keys['ArrowUp']) hero.position.z -= moveSpeed;
                    if (keys['ArrowDown']) hero.position.z += moveSpeed;
                    if (keys['ArrowLeft']) hero.position.x -= moveSpeed;
                    if (keys['ArrowRight']) hero.position.x += moveSpeed;
                }
                
                renderer.render(scene, camera);
            }
            
            animate();

            // Респонсивност
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
    </body>
    </html>
    """
    
    st.components.v1.html(html_code, height=600, scrolling=False)
    st.markdown("**Инструкции:** Кликнете върху 3D сцената, след което използвайте стрелките ↑ ↓ ← →")

if __name__ == "__main__":
    main()
