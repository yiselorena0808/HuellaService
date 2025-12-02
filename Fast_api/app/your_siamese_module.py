import numpy as np
from PIL import Image, ImageDraw
import os

# Carpeta raíz del dataset
dataset_dir = "dataset_example"

persons = ["person1", "person2"]

# Crear carpetas
for person in persons:
    os.makedirs(os.path.join(dataset_dir, person), exist_ok=True)

# Función para generar imagen sintética de huella
def generate_fake_fingerprint(save_path, seed=0):
    np.random.seed(seed)
    img = Image.new('L', (128, 128), color=255)  # Imagen en escala de grises
    draw = ImageDraw.Draw(img)
    
    # Dibujar líneas curvas simulando crestas
    for i in range(5, 120, 5):
        offset = np.random.randint(-2, 3)
        draw.arc([i, 0, i+60, 128], start=0, end=180, fill=0)
    
    # Agregar ruido aleatorio
    noise = np.random.randint(0, 30, (128, 128), dtype=np.uint8)
    img_array = np.array(img)
    img_array = np.clip(img_array - noise, 0, 255)
    img = Image.fromarray(img_array)
    
    img.save(save_path)

# Generar 2 huellas por persona
generate_fake_fingerprint(os.path.join(dataset_dir, "person1", "1.png"), seed=1)
generate_fake_fingerprint(os.path.join(dataset_dir, "person1", "2.png"), seed=2)
generate_fake_fingerprint(os.path.join(dataset_dir, "person2", "1.png"), seed=3)
generate_fake_fingerprint(os.path.join(dataset_dir, "person2", "2.png"), seed=4)

print("✅ Dataset de ejemplo generado en:", dataset_dir)