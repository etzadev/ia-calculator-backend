from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    try:
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    except Exception as e:
        print(f"Error al analizar la imagen: {e}")
        return {"message": "Error al procesar la imagen", "status": "error"}
    
    response_data = []
    for response in responses:
        response_data.append(response)
    print('respuesta en la ruta: ', response_data)
    return {"message": "Imagen procesada", "data": response_data, "status": "success"}
