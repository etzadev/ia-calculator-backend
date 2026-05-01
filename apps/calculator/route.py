from fastapi import APIRouter, HTTPException, Request
import base64
import binascii
import time
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 8
rate_limit_store: dict[str, list[float]] = {}

def enforce_rate_limit(client_id: str):
    now = time.time()
    recent_requests = [
        timestamp
        for timestamp in rate_limit_store.get(client_id, [])
        if now - timestamp < RATE_LIMIT_WINDOW_SECONDS
    ]

    if len(recent_requests) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Demasiadas solicitudes. Espera un minuto antes de volver a calcular.",
        )

    recent_requests.append(now)
    rate_limit_store[client_id] = recent_requests

@router.post('')
async def run(data: ImageData, request: Request):
    client_host = request.client.host if request.client else "unknown"
    enforce_rate_limit(client_host)

    try:
        if "," not in data.image:
            raise ValueError("La imagen debe venir en formato data URL base64.")

        image_data = base64.b64decode(data.image.split(",", 1)[1])
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
        image.verify()
        image = Image.open(BytesIO(image_data))
    except (ValueError, binascii.Error, OSError) as e:
        raise HTTPException(status_code=400, detail=f"Imagen invalida: {e}")

    try:
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    except Exception as e:
        error_message = str(e)
        print(f"Error al analizar la imagen: {type(e).__name__}: {error_message}", flush=True)

        if "GEMINI_API_KEY" in error_message:
            detail = "Falta configurar GEMINI_API_KEY en Railway."
        elif "API_KEY" in error_message or "api key" in error_message.lower():
            detail = "La API key de Gemini no es valida o no esta configurada."
        elif "NOT_FOUND" in error_message or "not found" in error_message.lower():
            detail = "El modelo Gemini configurado no existe o no soporta generateContent."
        elif "permission" in error_message.lower() or "permission_denied" in error_message.lower():
            detail = "Gemini rechazo la solicitud por permisos. Revisa la API key y que Gemini API este habilitada."
        elif "timeout" in error_message.lower() or "deadline" in error_message.lower():
            detail = "Gemini tardo demasiado en responder. Intenta con una seleccion mas pequena del canvas."
        elif "quota" in error_message.lower() or "rate" in error_message.lower():
            detail = "Gemini rechazo la solicitud por cuota o limite de frecuencia."
        else:
            detail = f"Error al procesar la imagen con Gemini: {error_message}"

        raise HTTPException(status_code=502, detail=detail)

    if not responses:
        raise HTTPException(
            status_code=422,
            detail="Gemini no devolvio una respuesta interpretable. Intenta escribir mas claro o selecciona solo el area del calculo.",
        )
    
    response_data = []
    for response in responses:
        response_data.append(response)
    print('respuesta en la ruta: ', response_data)
    return {"message": "Imagen procesada", "data": response_data, "status": "success"}
