"""
Chatbot con IA - Tarea
Usa la API de Google Gemini (gratis) para responder mensajes del usuario.

Antes de correr esto:
1. pip install google-genai python-dotenv
2. Crea un archivo .env en la misma carpeta con:
   GEMINI_API_KEY=tu_api_key_aqui
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

historial = []


def obtener_respuesta_ia(mensaje_usuario):
    historial.append(mensaje_usuario)
    respuesta = client.models.generate_content(
        model="gemini-flash-latest",
        contents=mensaje_usuario
    )
    return respuesta.text


def iniciar_chat():
    print("=== Chatbot con IA ===")
    print("Escribe 'salir' para terminar la conversación.\n")

    while True:
        entrada_usuario = input("Tú: ")

        if entrada_usuario.lower() == "salir":
            print("Chatbot: ¡Hasta luego!")
            break

        try:
            respuesta = obtener_respuesta_ia(entrada_usuario)
            print(f"Chatbot: {respuesta}\n")
        except Exception as error:
            print(f"Ocurrió un error: {error}\n")


if __name__ == "__main__":
    iniciar_chat()