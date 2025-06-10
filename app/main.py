from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Carga las preguntas desde el archivo JSON
with open("preguntas.json", "r", encoding="utf-8") as f:
    preguntas_respuestas = json.load(f)

def mezclar_opciones(pregunta):
    pregunta_mezclada = pregunta.copy()
    opciones = pregunta_mezclada["opciones"].copy()
    random.shuffle(opciones)
    pregunta_mezclada["opciones"] = opciones
    return pregunta_mezclada

def generar_test(num_preguntas):
    # Primero seleccionamos las preguntas al azar
    preguntas_seleccionadas = random.sample(preguntas_respuestas, min(num_preguntas, len(preguntas_respuestas)))
    # Luego mezclamos las opciones de cada pregunta
    return [mezclar_opciones(pregunta) for pregunta in preguntas_seleccionadas]

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "test.html",
        {
            "request": request,
            "preguntas": [],
            "preguntas_respuestas": preguntas_respuestas,
            "mostrar_resultados": False
        }
    )

@app.post("/generar", response_class=HTMLResponse)
async def generar_test_endpoint(request: Request, num_preguntas: int = Form(...)):
    preguntas = generar_test(num_preguntas)
    return templates.TemplateResponse(
        "test.html",
        {
            "request": request,
            "preguntas": preguntas,
            "preguntas_json": json.dumps(preguntas),
            "mostrar_resultados": False
        }
    )

@app.post("/evaluar", response_class=HTMLResponse)
async def evaluar(request: Request, preguntas_json: str = Form(...)):
    form_data = await request.form()
    preguntas = json.loads(preguntas_json)
    resultados = []

    for i, pregunta in enumerate(preguntas):
        correcta = pregunta["respuesta"]
        respuesta_usuario = form_data.get(f"respuesta_{i}", "")
        es_correcto = respuesta_usuario == correcta
        resultados.append({
            "pregunta": pregunta,
            "correcta": correcta,
            "respuesta_usuario": respuesta_usuario,
            "es_correcto": es_correcto
        })

    return templates.TemplateResponse(
        "test.html",
        {
            "request": request,
            "preguntas": preguntas,
            "resultados": resultados,
            "mostrar_resultados": True
        }
    )

