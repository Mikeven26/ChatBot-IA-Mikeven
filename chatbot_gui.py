import os
import math
import random
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from google import genai

# ---------- Paleta hacker (negro / verde matrix) ----------
NEGRO_FONDO = "#0a0e0a"
NEGRO_PANEL = "#0d1b0d"
VERDE_BRILLANTE = "#00ff41"
VERDE_OSCURO = "#0a5c1f"
VERDE_TEXTO_USUARIO = "#39ff6a"
FUENTE = "Consolas"

NOMBRE_BOT = "Lorenzo Linux"

# Cargar la API key desde el archivo .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- Estado de la animacion del gato ----------
frame_actual = 0
esta_parpadeando = False
contador_parpadeo = 0
proximo_parpadeo = random.randint(40, 100)
esta_pensando = False  # se pone True mientras espera la respuesta de la IA


def obtener_respuesta_ia(mensaje_usuario):
    """
    Recibe el mensaje del usuario, llama a la API de Gemini
    y devuelve la respuesta del modelo, en el "personaje" de Lorenzo Linux.
    """
    prompt_con_personalidad = (
        f"Actua como {NOMBRE_BOT}, un gato hacker experto en informatica, "
        "con un tono divertido, un poco presumido pero simpatico. "
        "Responde de forma breve y util. Mensaje del usuario: " + mensaje_usuario
    )

    respuesta = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt_con_personalidad
    )
    return respuesta.text


def enviar_mensaje(event=None):
    """
    Se ejecuta al presionar Enviar o Enter. Muestra el mensaje del usuario,
    llama a la IA y muestra la respuesta en el area de chat.
    """
    global esta_pensando

    mensaje = campo_entrada.get().strip()

    if mensaje == "":
        return

    area_chat.config(state="normal")
    area_chat.insert(tk.END, "Tu: " + mensaje + "\n\n", "usuario")
    area_chat.config(state="disabled")
    area_chat.see(tk.END)

    campo_entrada.delete(0, tk.END)

    esta_pensando = True
    ventana.update_idletasks()

    try:
        respuesta = obtener_respuesta_ia(mensaje)
    except Exception as error:
        respuesta = f"[error] {error}"

    esta_pensando = False

    area_chat.config(state="normal")
    area_chat.insert(tk.END, f"{NOMBRE_BOT}: " + respuesta + "\n\n", "bot")
    area_chat.config(state="disabled")
    area_chat.see(tk.END)


def dibujar_gato(canvas, offset_y=0, ojos_cerrados=False):
    """
    Dibuja el avatar del gato negro. offset_y mueve todo el dibujo
    verticalmente (para el efecto de "respiracion"). ojos_cerrados
    dibuja los ojos como lineas (parpadeo) en vez de circulos.
    """
    canvas.delete("all")
    y = offset_y

    # Cabeza
    canvas.create_oval(10, 20 + y, 70, 75 + y, fill="#000000", outline=VERDE_BRILLANTE, width=2)
    # Orejas
    canvas.create_polygon(12, 28 + y, 25, 5 + y, 35, 25 + y, fill="#000000", outline=VERDE_BRILLANTE, width=2)
    canvas.create_polygon(68, 28 + y, 55, 5 + y, 45, 25 + y, fill="#000000", outline=VERDE_BRILLANTE, width=2)
    canvas.create_polygon(17, 24 + y, 25, 12 + y, 30, 24 + y, fill=VERDE_OSCURO)
    canvas.create_polygon(63, 24 + y, 55, 12 + y, 50, 24 + y, fill=VERDE_OSCURO)

    # Ojos: abiertos (circulos) o cerrados (lineas, parpadeo)
    if ojos_cerrados:
        canvas.create_line(24, 45 + y, 34, 45 + y, fill=VERDE_BRILLANTE, width=2)
        canvas.create_line(46, 45 + y, 56, 45 + y, fill=VERDE_BRILLANTE, width=2)
    else:
        canvas.create_oval(24, 40 + y, 34, 50 + y, fill=VERDE_BRILLANTE, outline="")
        canvas.create_oval(46, 40 + y, 56, 50 + y, fill=VERDE_BRILLANTE, outline="")
        canvas.create_oval(27, 43 + y, 31, 47 + y, fill="#000000")
        canvas.create_oval(49, 43 + y, 53, 47 + y, fill="#000000")

    # Nariz
    canvas.create_polygon(37, 55 + y, 43, 55 + y, 40, 59 + y, fill=VERDE_BRILLANTE)
    # Bigotes
    canvas.create_line(5, 55 + y, 22, 57 + y, fill=VERDE_BRILLANTE)
    canvas.create_line(5, 62 + y, 22, 61 + y, fill=VERDE_BRILLANTE)
    canvas.create_line(58, 57 + y, 75, 55 + y, fill=VERDE_BRILLANTE)
    canvas.create_line(58, 61 + y, 75, 62 + y, fill=VERDE_BRILLANTE)


def animar_gato():
    """
    Bucle de animacion: se llama a si mismo cada 50ms.
    Mueve el gato con un efecto de "respiracion" (sube y baja suave)
    y lo hace parpadear cada cierto tiempo al azar.
    Si esta_pensando es True, parpadea mas rapido (se ve "ocupado").
    """
    global frame_actual, esta_parpadeando, contador_parpadeo, proximo_parpadeo

    frame_actual += 1

    # Efecto de respiracion (sube/baja suave)
    velocidad = 0.25 if esta_pensando else 0.1
    amplitud = 2 if esta_pensando else 3
    bounce = math.sin(frame_actual * velocidad) * amplitud

    # Logica del parpadeo
    if not esta_parpadeando:
        contador_parpadeo += 1
        limite = 15 if esta_pensando else proximo_parpadeo
        if contador_parpadeo >= limite:
            esta_parpadeando = True
            contador_parpadeo = 0
    else:
        contador_parpadeo += 1
        if contador_parpadeo >= 4:
            esta_parpadeando = False
            contador_parpadeo = 0
            proximo_parpadeo = random.randint(40, 100)

    dibujar_gato(canvas_gato, offset_y=bounce, ojos_cerrados=esta_parpadeando)

    ventana.after(50, animar_gato)


# ---------- Construccion de la ventana ----------

ventana = tk.Tk()
ventana.title(f"{NOMBRE_BOT} - Chatbot con IA")
ventana.geometry("500x620")
ventana.configure(bg=NEGRO_FONDO)

# Encabezado: avatar + nombre
marco_encabezado = tk.Frame(ventana, bg=NEGRO_FONDO, pady=10)
marco_encabezado.pack(fill=tk.X)

canvas_gato = tk.Canvas(
    marco_encabezado, width=80, height=85, bg=NEGRO_FONDO,
    highlightthickness=0
)
canvas_gato.pack(side=tk.LEFT, padx=(15, 10))

marco_texto_titulo = tk.Frame(marco_encabezado, bg=NEGRO_FONDO)
marco_texto_titulo.pack(side=tk.LEFT)

titulo = tk.Label(
    marco_texto_titulo,
    text=NOMBRE_BOT,
    font=(FUENTE, 18, "bold"),
    bg=NEGRO_FONDO,
    fg=VERDE_BRILLANTE
)
titulo.pack(anchor="w")

subtitulo = tk.Label(
    marco_texto_titulo,
    text="> gato hacker en linea_",
    font=(FUENTE, 10),
    bg=NEGRO_FONDO,
    fg=VERDE_OSCURO
)
subtitulo.pack(anchor="w")

# Area donde se muestra la conversacion
area_chat = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    font=(FUENTE, 11),
    bg=NEGRO_PANEL,
    fg=VERDE_BRILLANTE,
    insertbackground=VERDE_BRILLANTE,
    state="disabled",
    padx=10,
    pady=10,
    borderwidth=0,
    highlightthickness=1,
    highlightbackground=VERDE_OSCURO
)
area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

area_chat.tag_config("usuario", foreground=VERDE_TEXTO_USUARIO)
area_chat.tag_config("bot", foreground=VERDE_BRILLANTE)

# Fila de abajo: campo de texto + boton enviar
marco_inferior = tk.Frame(ventana, bg=NEGRO_FONDO)
marco_inferior.pack(padx=10, pady=(0, 15), fill=tk.X)

campo_entrada = tk.Entry(
    marco_inferior,
    font=(FUENTE, 12),
    bg=NEGRO_PANEL,
    fg=VERDE_BRILLANTE,
    insertbackground=VERDE_BRILLANTE,
    relief="flat"
)
campo_entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
campo_entrada.bind("<Return>", enviar_mensaje)
campo_entrada.focus()

boton_enviar = tk.Button(
    marco_inferior,
    text="ENVIAR",
    font=(FUENTE, 10, "bold"),
    bg=VERDE_BRILLANTE,
    fg="#000000",
    activebackground=VERDE_OSCURO,
    relief="flat",
    padx=15,
    command=enviar_mensaje
)
boton_enviar.pack(side=tk.RIGHT)

# Arrancar la animacion del gato y luego la ventana
animar_gato()
ventana.mainloop()