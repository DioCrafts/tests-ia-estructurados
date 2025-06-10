import os

# Estructura del proyecto
project_structure = {
    "app": {
        "main.py": """from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

preguntas_respuestas = [
    {"pregunta": "¿Cuál es la capital de Francia?", "opciones": ["París", "Madrid", "Roma", "Berlín"], "respuesta": "París"},
    {"pregunta": "¿Cuál es el resultado de 5 + 7?", "opciones": ["10", "12", "14", "16"], "respuesta": "12"},
    {"pregunta": "¿En qué continente está Brasil?", "opciones": ["Asia", "Europa", "América del Sur", "África"], "respuesta": "América del Sur"}
]

def generar_test(num_preguntas):
    return random.sample(preguntas_respuestas, num_preguntas)

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("test.html", {"request": request, "preguntas": [], "mostrar_resultados": False})

@app.post("/evaluar", response_class=HTMLResponse)
async def evaluar(request: Request, num_preguntas: int = Form(...), respuestas: list[str] = Form([])):
    preguntas = generar_test(num_preguntas)
    resultados = []
    for i, pregunta in enumerate(preguntas):
        correcta = pregunta["respuesta"]
        respuesta_usuario = respuestas[i] if i < len(respuestas) else ""
        es_correcto = respuesta_usuario == correcta
        resultados.append({"pregunta": pregunta, "correcta": correcta, "respuesta_usuario": respuesta_usuario, "es_correcto": es_correcto})
    return templates.TemplateResponse("test.html", {"request": request, "preguntas": preguntas, "resultados": resultados, "mostrar_resultados": True})
""",
        "templates": {
            "test.html": """<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Test Aleatorio</title>
</head>
<body>
    <h1>Generador de Tests</h1>
    <form method=\"post\" action=\"/evaluar\">
        {% if not mostrar_resultados %}
            <label for=\"num_preguntas\">Número de preguntas:</label>
            <input type=\"number\" name=\"num_preguntas\" min=\"1\" max=\"{{ preguntas | length }}\" required>
            <button type=\"submit\">Comenzar Test</button>
        {% else %}
            <h2>Resultados:</h2>
            <ul>
                {% for resultado in resultados %}
                    <li>
                        <strong>{{ resultado.pregunta[\"pregunta\"] }}</strong><br>
                        Tu respuesta: {{ resultado.respuesta_usuario }}<br>
                        {% if resultado.es_correcto %}
                            <span style=\"color: green;\">¡Correcto!</span>
                        {% else %}
                            <span style=\"color: red;\">Incorrecto (Correcta: {{ resultado.correcta }})</span>
                        {% endif %}
                    </li>
                {% endfor %}
            </ul>
            <a href=\"/\">Volver a intentar</a>
        {% endif %}
    </form>
</body>
</html>
"""
        }
    },
    "requirements.txt": "fastapi\nuvicorn\njinja2\n",
    "Dockerfile": """# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY ./app /app
COPY requirements.txt /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\", \"--reload\"]
"""
}

# Crear carpetas y archivos
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

if __name__ == "__main__":
    base_path = os.getcwd()  # Directorio actual
    create_structure(base_path, project_structure)
    print(f"Estructura del proyecto creada en: {base_path}")

