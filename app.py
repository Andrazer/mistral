from flask import Flask, render_template, request
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'file' not in request.files:
        return render_template('index.html', error='No se ha seleccionado ningún archivo.')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No se ha seleccionado ningún archivo.')

    if file:
        # Crea el directorio 'uploads' si no existe
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        # Guarda el archivo PDF en el servidor
        pdf_path = 'uploads/' + file.filename
        file.save(pdf_path)

        # Extrae el texto del PDF
        pdf_text = extract_text_from_pdf(pdf_path)

        # Extrae las imágenes del PDF de la primera página
        image_paths = extract_images_from_pdf(pdf_path)

        return render_template('index.html', pdf_text=pdf_text, image_paths=image_paths)

    return render_template('index.html', error='Error al procesar el archivo.')

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

    return text

def extract_images_from_pdf(pdf_path):
    image_paths = []

    with fitz.open(pdf_path) as pdf_document:
        # Extrae la primera página
        page = next(pdf_document.pages())

        # Extrae solo la primera imagen de la primera página
        images = page.get_images(full=True)
        img_info = next(iter(images), None)

        if img_info:
            img_index, _ = img_info[:2]
            img = pdf_document.extract_image(img_index)
            img_bytes = img["image"]

            # Guarda la imagen en el servidor
            image_path = f'uploads/page_{page.number + 1}_img_{img_index}.png'
            with open(image_path, "wb") as img_file:
                img_file.write(img_bytes)

            image_paths.append(image_path)

    return image_paths

if __name__ == '__main__':
    app.run(debug=True)
