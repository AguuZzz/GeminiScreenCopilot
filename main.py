import os
from pathlib import Path

import mss
from PIL import Image
from io import BytesIO
import pyttsx3
import time
import json

import google.generativeai as genai



with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.json", "r+") as json_file:
    conf = json.load(json_file)
    try:
      apikey = conf["apikey"]
      tokens = conf["tokens"]
      tiempo = conf["tiempoespera"]
      i = conf["nomodificar"]
    except:
      engine = pyttsx3.init()
      engine.say("Hubo un error al obtener una de las variantes dentro del archivo yeison en la carpeta del programa  , comprueba si estan bien configuradas o vuelve a descargar el archivo original del repositorio")
      engine.runAndWait()
      exit()
    if i == 0:
      engine = pyttsx3.init()
      engine.say("Bienvenido, antes de iniciar con el script, debes saber que puedes hacer un par de configuraciones basicas en el archivo config punto yeison, que se encuentra dentro de esta carpeta. A su vez hay un archivo punto text, donde se encuentra distinta informacion sobre el programa")
      engine.runAndWait()
      with open(f"{os.path.dirname(os.path.abspath(__file__))}/Leeme.txt", "w") as archivo:
        archivo.write("""Bienvenido a mi proyecto donde integro gemini en tu computadora sin interrumpir tu privacidad tal como lo hace copilot de Microsoft (una ai integrada con las mismas funcionalidades que este script)
la guia para obtener la "apikey" de gemini se encontrara dentro de mi repositorio de github:
https://github.com/AguuZzz/GeminiScreenCopilot
si de casualidad al ejecutar el programa otra vez te da el mensaje de bienvenida, modifica el config.json cambiando el "0" por "1"
""")
      conf["nomodificar"] = 1
      json_file.seek(0)
      json_file.truncate()
      json.dump(conf, json_file, indent=2)
      exit()
genai.configure(api_key=apikey)


time.sleep(tiempo)

try:
  with mss.mss() as sct:
      screenshot_path = "temp_screenshot.png"
      sct.shot(output=screenshot_path)


  with open(screenshot_path, "rb") as file:
      screenshot_bytes = file.read()

  os.remove(screenshot_path)
except:
  engine = pyttsx3.init()
  engine.say("Hubo un error al capturar y leer la pantalla, intentelo mas tarde. Si el programa sigue sin funcionar, comunicar al repositorio del proyecto que se encuentra en la carpeta del ejecutable")
  engine.runAndWait()

generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": tokens,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


image_parts = [
  {
    "mime_type": "image/png",
    "data": screenshot_bytes
  },
]

prompt_parts = [
  "Eres un asistente que analiza capturas de pantalla\nMira esta captura de pantalla cuidadosamente, tomate tu tiempo, y luego aporta informacion importante como ayuda, descripciones, definiciones o cosas importantes que el usario quiza no logre entender de lo que se encuentra en pantalla, traduce textos, explica imageness",
  image_parts[0],
]

response = model.generate_content(prompt_parts)
print(response.text)



   
engine = pyttsx3.init()
engine.say(response.text)
engine.runAndWait()