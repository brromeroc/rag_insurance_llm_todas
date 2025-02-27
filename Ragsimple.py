import PyPDF2
import ollama  # Asegúrate de tener este módulo correctamente configurado

def extraer_texto_pdf_paginas(pdf_path, paginas):
    """
    Extrae el texto de las páginas especificadas del PDF.
    `paginas` es una lista de índices (0-indexado).
    """
    texto = ""
    with open(pdf_path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        total_paginas = len(lector.pages)
        for num in paginas:
            if 0 <= num < total_paginas:
                pagina = lector.pages[num]
                texto += pagina.extract_text() + "\n"
            else:
                print(f"La página {num+1} no existe en el documento.")
    return texto

def main():
    # Ruta al PDF a leer
    pdf_path = "C:/Users/USUARIO/OneDrive/Escritorio/Trabajo Davivienda/Insurance-2030-The-impact-of-AI-on-the-future-of-insurance.pdf"
    
    # Pedir al usuario que ingrese los números de páginas (1-indexado) separados por coma
    paginas_input = input("Ingresa los números de las páginas que deseas analizar (máximo 4, separados por comas): ")
    try:
        # Convertir a lista de índices (0-indexado) y limitar a 3 páginas
        paginas = [int(x.strip()) - 1 for x in paginas_input.split(",") if x.strip().isdigit()]
        if not paginas:
            print("No se ingresaron números de página válidos.")
            return
        paginas = paginas[:4]
    except Exception as e:
        print("Error al procesar las páginas:", e)
        return

    # Extraer el texto de las páginas seleccionadas
    texto_seleccionado = extraer_texto_pdf_paginas(pdf_path, paginas)
    if not texto_seleccionado:
        print("No se pudo extraer texto de las páginas seleccionadas.")
        return
    print("Se han extraído las páginas seleccionadas correctamente.")

    # Permitir al usuario ingresar su pregunta o instrucción sobre el documento
    pregunta = input("Ingresa tu pregunta o instrucción sobre el documento: ")

    # Crear el cliente de Ollama y generar la respuesta usando el texto extraído
    client = ollama.Client()
    prompt = texto_seleccionado + "\n\n" + pregunta
    print("Procesando la consulta...")
    respuesta = client.generate(model="llama3.2", prompt=prompt)
    
    # Mostrar la respuesta
    print("\nRespuesta:")
    print(respuesta.response)

if __name__ == "__main__":
    main()