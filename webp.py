# -----------------------------------------------------------------------------
# © 2024 y2k (y2k@desarrollaria.com)
# Script para convertir imágenes .jpg, .jpeg y .png a .webp
# Sitio web: https://desarrollaria.com
# Cursos: https://generaria.com
# 
# Todos los derechos reservados.
# 
# -----------------------------------------------------------------------------

import os
import time
from PIL import Image

def convert_images(input_folder, output_folder):
    # Extensiones de archivos que queremos convertir
    valid_extensions = [".jpg", ".jpeg", ".png"]

    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Inicializar el contador de imágenes convertidas
    converted_count = 0

    # Iniciar el cronómetro
    start_time = time.time()

    # Recorrer todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        # Obtener la extensión del archivo
        ext = os.path.splitext(filename)[1].lower()

        # Procesar solo archivos con extensiones válidas
        if ext in valid_extensions:
            # Crear la ruta completa del archivo de entrada
            input_path = os.path.join(input_folder, filename)
            # Crear el nombre de archivo para la imagen convertida
            output_filename = os.path.splitext(filename)[0] + ".webp"
            output_path = os.path.join(output_folder, output_filename)
            
            # Abrir la imagen, convertirla a webp y guardarla en la carpeta de salida
            with Image.open(input_path) as img:
                img.save(output_path, "webp")
            
            print(f"Convertido: {input_path} -> {output_path}")
            
            # Incrementar el contador de imágenes convertidas
            converted_count += 1

    # Detener el cronómetro
    end_time = time.time()
    
    # Calcular el tiempo total transcurrido
    total_time = end_time - start_time

    # Mensaje de finalización
    print(f"\nConversión finalizada. Se convirtieron {converted_count} imágenes en {total_time:.2f} segundos.")

# Ruta de la carpeta de entrada (donde están las imágenes .jpg, .jpeg, .png)
input_folder = os.path.join(os.getcwd(), "ALL-IMG")

# Ruta de la carpeta de salida (donde se guardarán las imágenes convertidas)
output_folder = os.path.join(os.getcwd(), "WEBP")

# Llamar a la función de conversión
convert_images(input_folder, output_folder)
