import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()

class AIFitnessService:
    """
    Servicio para generar rutinas de ejercicios usando un modelo de IA
    """

    def __init__(self):
        self.token = os.getenv("AI_MODEL_TOKEN", "qlEE6b6b8fVXuRWYxAA8mxVDvfolkalv")
        self.model_url = os.getenv("AI_MODEL_URL", "https://mwjt5t5qmp2bhooiw2s7ioul.agents.do-ai.run/api/v1/chat/completions")
        self.model_name = os.getenv("AI_MODEL_NAME", "modifit-agent")

    def generate_exercises(self, user_prompt: str) -> Dict[str, Any]:
        """
        Genera ejercicios basados en el prompt del usuario

        Args:
            user_prompt: El prompt del usuario describiendo sus necesidades de entrenamiento

        Returns:
            Dict con los ejercicios generados y metadatos
        """
        try:
            # Preparar los datos para enviar al modelo de IA
            data = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 5000
            }

            # Configurar headers con Authorization Bearer
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }

            # Realizar la solicitud al modelo de IA
            response = requests.post(self.model_url, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()

                # Extraer el contenido de la respuesta
                if "choices" in result and len(result["choices"]) > 0:
                    ai_response = result["choices"][0]["message"]["content"]

                    # Parsear la respuesta para extraer los ejercicios
                    exercises = self._parse_exercises_from_response(ai_response)

                    return {
                        "status": "success",
                        "raw_response": ai_response,
                        "exercises": exercises,
                        "message": "Rutina generada exitosamente"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Respuesta inválida del modelo",
                        "raw_response": result
                    }
            else:
                return {
                    "status": "error",
                    "message": f"Error {response.status_code}: {response.text}",
                    "error_code": response.status_code
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al generar ejercicios: {str(e)}",
                "error_details": str(e)
            }

    def _parse_exercises_from_response(self, ai_response: str) -> List[Dict[str, Any]]:
        """
        Parsea la respuesta del modelo de IA para extraer los ejercicios

        Args:
            ai_response: La respuesta de texto del modelo de IA

        Returns:
            Lista de ejercicios parseados
        """
        exercises = []

        try:
            # Intentar parsear como JSON si la respuesta contiene JSON
            if "{" in ai_response and "}" in ai_response:
                # Encontrar el JSON en la respuesta
                json_start = ai_response.find("{")
                json_end = ai_response.rfind("}") + 1

                if json_start != -1 and json_end != 0:
                    json_str = ai_response[json_start:json_end]
                    try:
                        parsed = json.loads(json_str)

                        # Si es una lista de ejercicios
                        if isinstance(parsed, list):
                            exercises = parsed
                        # Si es un dict con ejercicios
                        elif isinstance(parsed, dict):
                            if "exercises" in parsed:
                                exercises = parsed["exercises"]
                            elif "routines" in parsed:
                                exercises = parsed["routines"]
                            else:
                                exercises = [parsed]
                    except json.JSONDecodeError:
                        # Si no es JSON válido, lo tratamos como texto plano
                        exercises = self._parse_text_exercises(ai_response)
            else:
                # Parsear como texto plano
                exercises = self._parse_text_exercises(ai_response)

        except Exception as e:
            # Si algo falla, retornar la respuesta como un único ejercicio
            exercises = [{
                "name": "Rutina generada",
                "description": ai_response,
                "is_text_response": True
            }]

        return exercises

    def _parse_text_exercises(self, text: str) -> List[Dict[str, Any]]:
        """
        Parsea ejercicios desde texto plano
        Busca líneas que comiencen con números o guiones

        Args:
            text: Texto con los ejercicios

        Returns:
            Lista de ejercicios parseados
        """
        exercises = []
        lines = text.split('\n')

        current_exercise = None
        for line in lines:
            line = line.strip()

            # Saltar líneas vacías
            if not line:
                if current_exercise:
                    exercises.append(current_exercise)
                    current_exercise = None
                continue

            # Detectar nueva línea de ejercicio (comienza con número o guión)
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                if current_exercise:
                    exercises.append(current_exercise)

                # Crear nuevo ejercicio
                exercise_name = line.lstrip('0123456789.-• ').split(':')[0].split(',')[0]
                current_exercise = {
                    "name": exercise_name,
                    "description": line,
                    "series": 3,
                    "reps": 10
                }
            elif current_exercise:
                # Agregar información adicional al ejercicio actual
                current_exercise["description"] = f"{current_exercise['description']} {line}"

        # Agregar el último ejercicio
        if current_exercise:
            exercises.append(current_exercise)

        # Si no hay ejercicios parseados, retornar el texto completo como un ejercicio
        if not exercises:
            exercises = [{
                "name": "Rutina personalizada",
                "description": text,
                "is_text_response": True
            }]

        return exercises
