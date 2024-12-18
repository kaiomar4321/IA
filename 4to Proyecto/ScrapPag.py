import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_text_from_webpage(url):
    try:
        # Realiza la solicitud a la página web
        response = requests.get(url)
        response.raise_for_status()  # Verifica errores en la solicitud
        
        # Analiza el contenido HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extrae el texto principal (ignorando scripts, estilos, etc.)
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        
        text = soup.get_text(separator="\n")
        
        # Limpia el texto y elimina líneas en blanco adicionales
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)
        
        # Obtén el nombre base del dominio para el archivo
        parsed_url = urlparse(url)
        base_name = parsed_url.netloc.replace("www.", "")
        output_file = f"{base_name}.txt"
        
        # Guarda el contenido en un archivo
        with open(output_file, "w", encoding="utf-8") as text_file:
            text_file.write(clean_text)
        
        print(f"El contenido de la página web se ha guardado en {output_file}.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página web: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Cambia 'https://ejemplo.com' por la URL de la página que quieras procesar
url = "https://animalpolitico.com/politica/eleccion-jueces-reforma-judicial-crimen-violencia"
extract_text_from_webpage(url)
