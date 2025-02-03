# IA Calculator Backend

## Descripción

El backend de IA Calculator es una API desarrollada con FastAPI que procesa imágenes y realiza cálculos matemáticos a partir de las expresiones dibujadas en el frontend. Utiliza modelos generativos de inteligencia artificial para resolver las expresiones y devolver los resultados al frontend.

## Características

- **FastAPI**: Marco web rápido y de alto rendimiento para construir la API.
- **Procesamiento de Imágenes**: Decodificación y análisis de imágenes base64.
- **Modelos de IA**: Utiliza modelos generativos de Google para resolver expresiones matemáticas.
- **CORS Middleware**: Configuración de CORS para permitir solicitudes seguras entre el frontend y el backend.
- **Manejo de Errores**: Captura y manejo adecuado de errores para garantizar una respuesta adecuada y clara.

## Requisitos

- Python 3.x
- pip

## Instalación

1. Clona el repositorio:

   ```sh
   git clone https://github.com/etzadev/ia-calculator-backend.git
   cd ia-calculator-backend
   ```

2. Crea un entorno virtual e instala las dependencias:

   ```sh
   python -m venv virtual
   source virtual/bin/activate # En Windows usa `virtual\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Ejecuta el servidor FastAPI:

   ```sh
   uvicorn main:app --reload
   ```

## Endpoints

### `POST /calculate`

- **Descripción**: Recibe una imagen en formato base64 y un diccionario de variables, procesa la imagen y devuelve los resultados de los cálculos.
- **Cuerpo de la Solicitud**:

  ```json
  {
    "image": "data:image/png;base64,...",
    "dict_of_vars": {
      "x": 5,
      "y": 10
    }
  }
  ```

- **Ejemplo de Respuesta**:

  ```json
  {
    "message": "Imagen procesada",
    "data": [
      {
        "expr": "x = 5",
        "result": 5,
        "assign": true
      },
      {
        "expr": "y = 10",
        "result": 10,
        "assign": true
      },
      {
        "expr": "z = x + y",
        "result": 15,
        "assign": true
      }
    ],
    "status": "success"
  }
  ```

## Uso

1. Inicia el servidor FastAPI utilizando `uvicorn`.
2. Realiza solicitudes `POST` al endpoint `/calculate` con una imagen en formato base64 y el diccionario de variables necesarias.
3. Recibe los resultados de los cálculos en la respuesta de la API.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos para contribuir:

1. Haz un fork del repositorio.
2. Crea una rama con tu nueva funcionalidad: `git checkout -b mi-nueva-funcionalidad`
3. Realiza los cambios y haz commit: `git commit -m 'Añadir nueva funcionalidad'`
4. Sube los cambios a tu rama: `git push origin mi-nueva-funcionalidad`
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
