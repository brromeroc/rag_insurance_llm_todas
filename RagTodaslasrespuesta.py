import PyPDF2
import ollama

def extraer_texto_pdf(ruta_pdf):
    """Extrae y retorna el texto completo de un archivo PDF."""
    texto = ""
    with open(ruta_pdf, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def chunk_text(text, chunk_size=8000, overlap=400):
    """
    Divide el texto en chunks de tamaño fijo.
    Se puede ajustar chunk_size y overlap según el modelo.
    """
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # avance con solapamiento
    return chunks

def main():
    # Ruta al PDF a leer
    pdf_path = "C:/Users/USUARIO/OneDrive/Escritorio/Trabajo Davivienda/Insurance-2030-The-impact-of-AI-on-the-future-of-insurance.pdf"
    
    # Extraer el texto del PDF
    texto_pdf = extraer_texto_pdf(pdf_path)
    print("El contenido del PDF se ha cargado correctamente.")
    
    # Dividir el texto en chunks para procesar por partes
    chunks = chunk_text(texto_pdf)
    print(f"El documento se ha dividido en {len(chunks)} chunks.")
    
    # Permitir al usuario ingresar su pregunta o instrucción sobre el documento
    pregunta = input("Ingresa tu pregunta o instrucción sobre el documento: ")
    
    # Crear el cliente de Ollama
    client = ollama.Client()
    respuestas_chunks = []
    
    # Procesar cada chunk con la pregunta y almacenar la respuesta correspondiente
    for i, chunk in enumerate(chunks):
        prompt = chunk + "\n\n" + pregunta 
        print(f"Procesando chunk {i+1}/{len(chunks)}...")
        respuesta = client.generate(model="llama3.2", prompt=prompt)
        respuestas_chunks.append(respuesta.response)
    
    # Mostrar la respuesta de cada chunk por separado
    print("\nRespuestas por chunk:")
    for i, resp in enumerate(respuestas_chunks):
        print(f"\nRespuesta Chunk {i+1}:")
        print(resp)

if __name__ == "__main__":
    main()