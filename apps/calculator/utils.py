import google.generativeai as genai
import ast
import json
from PIL import Image
from constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
        f"Se te ha dado una imagen con algunas expresiones matemáticas, ecuaciones o problemas gráficos, y necesitas resolverlas. "
        f"Nota: Usa la regla PEMDAS para resolver expresiones matemáticas. PEMDAS significa el orden de prioridad: Paréntesis, Exponentes, Multiplicación y División (de izquierda a derecha), Suma y Resta (de izquierda a derecha). Los paréntesis tienen la máxima prioridad, seguidos por los Exponentes, luego la Multiplicación y División, y por último la Suma y Resta. "
        f"Por ejemplo: "
        f"P. 2 + 3 * 4 "
        f"(3 * 4) => 12, 2 + 12 = 14. "
        f"P. 2 + 3 + 5 * 4 - 8 / 2 "
        f"5 * 4 => 20, 8 / 2 => 4, 2 + 3 => 5, 5 + 20 => 25, 25 - 4 => 21. "
        f"PUEDES TENER CINCO TIPOS DE ECUACIONES/EXPRESIONES EN ESTA IMAGEN, Y SOLO UN CASO SE APLICARÁ CADA VEZ: "
        f"Los casos son los siguientes: "
        f"1. Expresiones matemáticas simples como 2 + 2, 3 * 4, 5 / 6, 7 - 8, etc.: En este caso, resuelve y devuelve la respuesta en el formato de una LISTA DE UN DICCIONARIO [{{'expr': expresión dada, 'result': respuesta calculada}}]. "
        f"2. Conjunto de ecuaciones como x^2 + 2x + 1 = 0, 3y + 4x = 0, 5x^2 + 6y + 7 = 12, etc.: En este caso, resuelve para la variable dada, y el formato debe ser una LISTA DE DICCIONARIOS SEPARADOS POR COMAS, con dict 1 como {{'expr': 'x', 'result': 2, 'assign': True}} y dict 2 como {{'expr': 'y', 'result': 5, 'assign': True}}. Este ejemplo asume que x se calculó como 2 y y como 5. Incluye tantos diccionarios como variables haya. "
        f"3. Asignación de valores a variables como x = 4, y = 5, z = 6, etc.: En este caso, asigna valores a las variables y devuelve otra clave en el diccionario llamada {{'assign': True}}, manteniendo la variable como 'expr' y el valor como 'result' en el diccionario original. DEVUELVE COMO UNA LISTA DE DICCIONARIOS. "
        f"4. Analizando problemas matemáticos gráficos, que son problemas de palabras representados en forma de dibujo, como colisiones de autos, problemas trigonométricos, problemas sobre el teorema de Pitágoras, suma de carreras en un gráfico de cricket, etc. Estos tendrán un dibujo que representa algún escenario y la información acompañante con la imagen. PRESTA MUCHA ATENCIÓN A LOS DIFERENTES COLORES EN ESTOS PROBLEMAS. Necesitas devolver la respuesta en el formato de UNA LISTA DE UN DICCIONARIO [{{'expr': expresión dada, 'result': respuesta calculada}}]. "
        f"5. Detección de conceptos abstractos que un dibujo podría mostrar, como amor, odio, celos, patriotismo, o una referencia histórica a la guerra, invención, descubrimiento, cita, etc. USA EL MISMO FORMATO QUE LOS OTROS PARA DEVOLVER LA RESPUESTA, donde 'expr' será la explicación del dibujo, y 'result' será el concepto abstracto. "
        f"Analiza la ecuación o expresión en esta imagen y devuelve la respuesta según las reglas dadas: "
        f"Asegúrate de usar barras invertidas adicionales para caracteres de escape como \\f -> \\\\f, \\n -> \\\\n, etc. "
        f"Aquí tienes un diccionario de variables asignadas por el usuario. Si la expresión dada tiene alguna de estas variables, usa su valor real de este diccionario en consecuencia: {dict_of_vars_str}. "
        f"NO USES COMILLAS INVERTIDAS NI FORMATO MARKDOWN. "
        f"USA COMILLAS ADECUADAS PARA LAS CLAVES Y VALORES EN EL DICCIONARIO PARA FACILITAR EL ANÁLISIS CON ast.literal_eval de Python."
    )
    response = model.generate_content([prompt, img])
    print(response.text)
    answers = []
    try:
        response_text = response.text.replace('null', 'None')  # Reemplaza null con None
        answers = ast.literal_eval(response_text)
    except Exception as e:
        print(f"Error al analizar la respuesta de la API de Gemini: {e}")
    print('respuesta devuelta ', answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers
