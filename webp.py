# -----------------------------------------------------------------------------
# Creado x: y2k  - Email: (y2k@desarrollaria.com)
# Script para convertir imágenes .jpg, .jpeg y .png a .webp
# Sitio web: https://desarrollaria.com
# Cursos: https://generaria.com
# 
# Todos los derechos reservados © 2024.
# 
# -----------------------------------------------------------------------------
import os
import time
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END, filedialog, messagebox, IntVar, Checkbutton, Frame
from PIL import Image, ImageTk, ImageOps
import pystray
from pystray import MenuItem as item
import sys
from threading import Timer

def convert_images(input_folder, output_folder, log_text, resize=False, keep_aspect_ratio=False, new_width=0, new_height=0):
    valid_extensions = [".jpg", ".jpeg" , ".png"]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    converted_count = 0
    start_time = time.time()

    for filename in os.listdir(input_folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_extensions:
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".webp"
            output_path = os.path.join(output_folder, output_filename)
            try:
                with Image.open(input_path) as img:
                    if resize:
                        if keep_aspect_ratio:
                            # Redimensionar manteniendo la proporción
                            if new_width > 0 and new_height == 0:
                                aspect_ratio = img.height / img.width
                                new_height = int(new_width * aspect_ratio)
                            elif new_height > 0 and new_width == 0:
                                aspect_ratio = img.width / img.height
                                new_width = int(new_height * aspect_ratio)
                        # Redimensionar sin mantener la proporción
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    img.save(output_path, "webp", quality=85)
                log_text.insert(END, f"Convertido: {input_path} -> {output_path}\n", "log_text_style")
            except Exception as e:
                log_text.insert(END, f"Error al convertir {input_path}: {str(e)}\n", "log_text_style")
            converted_count += 1

    end_time = time.time()
    total_time = end_time - start_time
    log_text.insert(END, f"\nConversión finalizada. Se convirtieron {converted_count} imágenes en {total_time:.2f} segundos.\n", "log_text_style")
    log_text.see(END)

def select_input_folder():
    folder = filedialog.askdirectory(title="Selecciona la carpeta de imágenes")
    if folder:
        input_folder_var.set(folder)

def select_output_folder():
    folder = filedialog.askdirectory(title="Selecciona la carpeta de salida")
    if folder:
        output_folder_var.set(folder)

def start_conversion():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    resize = resize_var.get()
    keep_aspect_ratio = aspect_ratio_var.get()

    # Validar y convertir valores de ancho y alto
    try:
        new_width = int(width_var.get().strip()) if width_var.get().strip() else 0
    except ValueError:
        new_width = 0

    try:
        new_height = int(height_var.get().strip()) if height_var.get().strip() else 0
    except ValueError:
        new_height = 0

    if not input_folder or not output_folder:
        messagebox.showwarning("Advertencia", "Debe seleccionar ambas carpetas (de entrada y salida).")
        return
    
    if resize and (new_width <= 0 and new_height <= 0) and not keep_aspect_ratio:
        messagebox.showwarning("Advertencia", "Debe especificar dimensiones válidas para el redimensionamiento.")
        return

    log_text.delete(1.0, END)
    log_text.insert(END, "Iniciando la conversión...\n", "log_text_style")
    convert_images(input_folder, output_folder, log_text, resize, keep_aspect_ratio, new_width, new_height)

def minimize_window(icon, item):
    app.withdraw()  # Oculta la ventana principal

def restore_window(icon, item):
    app.deiconify()  # Muestra la ventana principal

def quit_app(icon, item):
    icon.stop()  # Detiene el icono de la bandeja
    app.quit()   # Cierra la aplicación

def setup_tray_icon():
    icon_image = Image.open("img/favicon.ico")
    icon_image = ImageOps.fit(icon_image, (16, 16), Image.Resampling.LANCZOS)
    icon = pystray.Icon("name", icon_image, menu=pystray.Menu(
        item('Abrir', restore_window),
        item('Cerrar', quit_app)
    ))
    icon.run_detached()

app = Tk()
app.title("Conversor de Imágenes a WebP")
app.geometry("770x770")
app.configure(bg="#171717")

# Set the favicon.ico
app.iconbitmap("img/favicon.ico")

# Crear un borde para la ventana
border_frame = Frame(app, bg="#171717", bd=1)
border_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Hacer la ventana sin marco para poder crear una barra de título personalizada
app.overrideredirect(True)  # Quitar la barra de título estándar

# Crear una barra de título personalizada
title_bar = Frame(border_frame, bg="#2b2a33", relief="flat", bd=0)
title_bar.pack(fill="x", side="top")

# Agregar el favicon a la barra de título
favicon_img = Image.open("img/favicon.ico")
favicon_img = favicon_img.resize((16, 16), Image.Resampling.LANCZOS)
favicon_photo = ImageTk.PhotoImage(favicon_img)
favicon_label = Label(title_bar, image=favicon_photo, bg="#2b2a33")
favicon_label.pack(side="left", padx=10)

# Agregar un botón para cerrar la ventana en la barra de título
close_button = Button(title_bar, text="X", command=lambda: (app.quit(), app.destroy()), bg="#ff4c4c", fg="#ffffff", relief="flat", padx=5, pady=2)
close_button.pack(side="right", padx=5)

# Agregar un botón para minimizar la ventana en la barra de título
minimize_button = Button(title_bar, text="_", command=lambda: app.withdraw(), bg="#f7c030", fg="#ffffff", relief="flat", padx=5, pady=2)
minimize_button.pack(side="right", padx=5)

# Agregar un botón para maximizar la ventana en la barra de título
maximize_button = Button(title_bar, text="◻", command=lambda: app.state("zoomed") if app.state() == "normal" else app.state("normal"), bg="#4CAF50", fg="#ffffff", relief="flat", padx=5, pady=2)
maximize_button.pack(side="right", padx=5)

# Agregar el título a la barra de título
title_label = Label(title_bar, text="Zebra - IMG a WebP", font=("Arial", 10, "normal"), bg="#2b2a33", fg="#ffffff")
title_label.pack(side="left", padx=10)

# Función para mover la ventana personalizada
def move_window(event):
    app.geometry(f'+{event.x_root}+{event.y_root}')

title_bar.bind("<B1-Motion>", move_window)

# Contenido de la ventana
main_frame = Frame(border_frame, bg="#171717")  # Asegúrate de que el color de fondo esté configurado
main_frame.pack(pady=10, padx=20, fill="both", expand=True)

# logo
logo_img = Image.open("img/logo.png")
logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = Label(main_frame, image=logo_photo, bg="#171717")
logo_label.pack(pady=10)

# input frame
input_frame = Frame(main_frame, bg="#171717")  # Fondo oscuro para la coherencia
input_frame.pack(pady=10, padx=20, fill="x")

input_label = Label(input_frame, text="Carpeta de imágenes:", anchor="w", bg="#171717", fg="#ffffff")
input_label.grid(row=0, column=0, sticky='w')

input_folder_var = Entry(input_frame, width=50, bg="#333333", fg="#ffffff", insertbackground="white")
input_folder_var.insert(0, os.path.join(os.getcwd(), "ALL-IMG"))
input_folder_var.grid(row=0, column=1, padx=10)

input_button = Button(input_frame, text="Seleccionar", command=select_input_folder, bg="#2b2a33", fg="#ffffff", relief="solid", padx=10, pady=5)
input_button.grid(row=0, column=2, padx=5)

output_label = Label(input_frame, text="Carpeta de salida:", anchor="w", bg="#171717", fg="#ffffff")
output_label.grid(row=1, column=0, sticky='w')

output_folder_var = Entry(input_frame, width=50, bg="#333333", fg="#ffffff", insertbackground="white")
output_folder_var.insert(0, os.path.join(os.getcwd(), "WEBP"))
output_folder_var.grid(row=1, column=1, padx=10)

output_button = Button(input_frame, text="Seleccionar", command=select_output_folder, bg="#2b2a33", fg="#ffffff", relief="solid", padx=10, pady=5)
output_button.grid(row=1, column=2, padx=5)

# resize frame
resize_frame = Frame(main_frame, bg="#171717")  # Fondo oscuro para la coherencia
resize_frame.pack(pady=10, padx=20, fill="x")

resize_var = IntVar()
resize_check = Checkbutton(resize_frame, text="Redimensionar imágenes", variable=resize_var, bg="#171717", fg="#ffffff", selectcolor="#2b2a33")
resize_check.grid(row=0, column=0, sticky='w')

aspect_ratio_var = IntVar()
aspect_ratio_check = Checkbutton(resize_frame, text="Mantener proporción", variable=aspect_ratio_var, bg="#171717", fg="#ffffff", selectcolor="#2b2a33")
aspect_ratio_check.grid(row=0, column=1, sticky='w')

width_label = Label(resize_frame, text="Nuevo ancho:", anchor="w", bg="#171717", fg="#ffffff")
width_label.grid(row=1, column=0, sticky='w')

width_var = Entry(resize_frame, width=10, bg="#333333", fg="#ffffff", insertbackground="white")
width_var.grid(row=1, column=1, padx=10)

height_label = Label(resize_frame, text="Nueva altura:", anchor="w", bg="#171717", fg="#ffffff")
height_label.grid(row=2, column=0, sticky='w')

height_var = Entry(resize_frame, width=10, bg="#333333", fg="#ffffff", insertbackground="white")
height_var.grid(row=2, column=1, padx=10)

# log frame
log_frame = Frame(main_frame, bg="#171717")  # Fondo oscuro para la coherencia
log_frame.pack(pady=10, padx=20, fill="both", expand=True)

log_label = Label(log_frame, text="Registro de conversiones:", anchor="w", bg="#171717", fg="#ffffff")
log_label.pack(side="top", anchor="w")

log_text = Text(log_frame, height=15, bg="#333333", fg="#ffffff", insertbackground="white", wrap="word")
log_text.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(log_frame, command=log_text.yview, bg="#171717")
scrollbar.pack(side="right", fill="y")
log_text.config(yscrollcommand=scrollbar.set)

# Botón Iniciar Conversión
start_button = Button(main_frame, text="Iniciar Conversión", command=start_conversion, bg="#2b2a33", fg="#ffffff", relief="solid", padx=15, pady=10)
start_button.pack(pady=10)

# Agregar la barra de copyright en la parte inferior
copyright_frame = Frame(border_frame, bg="#171717", relief="flat", bd=0)
copyright_frame.pack(side="bottom", fill="x")

copyright_label = Label(copyright_frame, text="Todos los derechos reservados © 2024\nWeb: https://DesarrollarIA.com | Cursos: https://GenerarIA.com\nCreado x: y2k" , bg="#171717", fg="#ffffff", anchor="center", justify="center")
copyright_label.pack(pady=5)

# Iniciar el icono en la bandeja del sistema en segundo plano
setup_tray_icon()

app.mainloop()
