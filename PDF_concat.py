import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os
from reportlab.lib.pagesizes import letter
from PIL import Image
from reportlab.pdfgen import canvas
import img2pdf

# pyinstaller --onefile PDF_concat.py


# Juntar PDF's Función antigua
"""
def merge_pdfs(order='asc'):
    # Seleccionar los archivos PDF
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    
    if not file_paths:
        return
    
    # Ordenar los archivos por fecha
    reverse_order = (order == 'desc')
    file_paths = sorted(file_paths, key=lambda x: os.path.getmtime(x), reverse=reverse_order)
    
    merged_pdf = PdfMerger()
    
    # Combinar los archivos PDF
    for file_path in file_paths:
        merged_pdf.append(file_path)
    
    # Guardar el archivo combinado
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_path:
        with open(output_path, "wb") as output_file:
            merged_pdf.write(output_file)
        print("PDFs combinados exitosamente.")
    else:
        print("Operación cancelada.")
"""

# Convertir imagenes to PDF
def convertir_imagen_to_pdf(ruta_imagen):
    imagen = Image.open(ruta_imagen)
    pdf_ruta = ruta_imagen.replace(".jpg", ".pdf").replace(".png", ".pdf")
    imagen.save(pdf_ruta, "PDF", resolution=100.0)
    return pdf_ruta


def convert_images_to_pdfs():
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png")])
    if not image_paths:
        return

    pdf_paths = []
    for image_path in image_paths:
        pdf_path = convertir_imagen_to_pdf(image_path)
        pdf_paths.append(pdf_path)

    if pdf_paths:
        print("Imágenes convertidas a PDFs exitosamente.")
    else:
        print("No se seleccionaron imágenes.")

# Juntar imagenes y convertirlas a PDF
def merge_images_to_pdf():
    # Solicitar al usuario que seleccione las imágenes
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png")])
    if not image_paths:
        return

    # Verificar si todas las imágenes tienen el mismo tamaño
    first_image = Image.open(image_paths[0])
    first_width, first_height = first_image.size
    for image_path in image_paths[1:]:
        image = Image.open(image_path)
        if image.size != (first_width, first_height):
            messagebox.showwarning("Advertencia", "Todas las imágenes deben tener el mismo tamaño.")
            return

    # Solicitar al usuario que seleccione la ubicación y el nombre del archivo PDF resultante
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return

    # Crear un lienzo para el PDF con el tamaño de la página "letter"
    c = canvas.Canvas(output_path, pagesize=letter)

    # Agregar cada imagen al PDF
    for image_path in image_paths:
        # Dibujar la imagen en el lienzo del PDF
        c.drawImage(image_path, 0, 0, first_width, first_height)
        # Agregar una nueva página después de cada imagen
        c.showPage()

    # Guardar el archivo PDF
    c.save()
    print("Imágenes combinadas en un solo PDF exitosamente.")

#Convertir BMP to PDF
def convertir_imagenBMP_to_pdf(ruta_imagen):
    pdf_ruta = ruta_imagen.replace(".bmp", ".pdf")
    with open(pdf_ruta, "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(ruta_imagen))
    return pdf_ruta

def convert_bmp_to_pdf(bmp_paths):
    pdf_paths = []
    for bmp_path in bmp_paths:
        pdf_path = convertir_imagenBMP_to_pdf(bmp_path)
        pdf_paths.append(pdf_path)
    if pdf_paths:
        print("Imágenes BMP convertidas a PDFs exitosamente.")
    else:
        print("No se seleccionaron imágenes BMP.")

# Selccionar imagenes BMP
def select_bmp_images():
    bmp_paths = filedialog.askopenfilenames(filetypes=[("BMP files", "*.bmp")])
    if not bmp_paths:
        return
    convert_bmp_to_pdf(bmp_paths)


# Función interna para combinar PDFs
def combine_pdfs(order):
    # Seleccionar los archivos PDF
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        
    if not file_paths:
        return
        
    # Ordenar los archivos por fecha
    reverse_order = (order == 'desc')
    file_paths = sorted(file_paths, key=lambda x: os.path.getmtime(x), reverse=reverse_order)
        
    merged_pdf = PdfMerger()
        
    # Combinar los archivos PDF
    for file_path in file_paths:
        merged_pdf.append(file_path)
        
    # Guardar el archivo combinado
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if output_path:
        with open(output_path, "wb") as output_file:
            merged_pdf.write(output_file)
        print("PDFs combinados exitosamente.")
    else:
        print("Operación cancelada.")


# Crear ventana para seleccionar orden
def select_order():
    order_window = tk.Toplevel(root)
    order_window.title("Seleccionar orden")
    order_window.geometry("300x100")
        
    # Funciones para botones de orden ascendente y descendente
    def merge_asc():
        order_window.destroy()
        combine_pdfs('asc')
        
    def merge_desc():
        order_window.destroy()
        combine_pdfs('desc')
        
    # Botones de orden
    asc_button = tk.Button(order_window, text="Ascendente (Viejo->Nuevo)", command=merge_asc)
    asc_button.pack(pady=10)
       
    desc_button = tk.Button(order_window, text="Descendente (Nuevo->Viejo)", command=merge_desc)
    desc_button.pack(pady=10)

# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Aplicación editor PDF")
root.geometry("350x250")
print("Version 1.2.1")

# Botón para juntar PDFs
merge_button = tk.Button(root, text="Juntar PDFs", command=select_order)
merge_button.pack(pady=20)

"""
# Botón para combinar los PDFs en orden ascendente
merge_button_asc = tk.Button(root, text="Elige los PDFs Ascendente (Viejo->Nuevo)", command=lambda: merge_pdfs(order='asc'))
merge_button_asc.pack(pady=10)

# Botón para combinar los PDFs en orden descendente
merge_button_desc = tk.Button(root, text="Elige los PDFs Descendente (Nuevo->Viejo)", command=lambda: merge_pdfs(order='desc'))
merge_button_desc.pack(pady=10)"""


# Botón para convertir imágenes a PDFs
convert_button = tk.Button(root, text="Convertir imagen/s a PDF/s", command=convert_images_to_pdfs)
convert_button.pack(pady=10)

# Crear el botón para seleccionar imágenes BMP
bmp_button = tk.Button(root, text="Seleccionar imágenes BMP y convertir PDF", command=select_bmp_images)
bmp_button.pack(pady=10)

# Botón para combinar imágenes en un solo PDF
merge_button = tk.Button(root, text="Combinar varias imágenes en un solo PDF", command=merge_images_to_pdf)
merge_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
