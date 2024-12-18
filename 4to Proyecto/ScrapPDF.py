import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        # Verifica si el archivo existe
        if not os.path.exists(pdf_path):
            print(f"El archivo {pdf_path} no existe.")
            return
        
        # Extrae el nombre base del archivo sin extensión
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_file = f"{base_name}.txt"
        
        # Abre el PDF y extrae el texto
        reader = PdfReader(pdf_path)
        with open(output_file, "w", encoding="utf-8") as text_file:
            for page in reader.pages:
                text_file.write(page.extract_text())
                text_file.write("\n")  # Agrega un salto de línea entre páginas
        
        print(f"El texto del PDF se ha guardado en {output_file}.")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Cambia 'tu_archivo.pdf' por el nombre del archivo PDF que deseas procesar
pdf_path = "PDF/PoderJudicial1.pdf"
extract_text_from_pdf(pdf_path)
