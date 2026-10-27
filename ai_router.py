import os

from google import genai
from google.genai import types
from groq import Groq
from makro_manager import MacroManager
import json

class AIRouter:
    def __init__(self):
        self.client = Groq()

        # sztuczna lista dostepnych makr
        self.available_makros = {
            "kalkulator": "otwiera kalkulator systemowy",
            "test": "wykonuje test działania makr",
            "umrzyj": "wyłącza komputer",
            "otworz_przegladarke":"otwiera przegladarke internetowa"
        }

    def route_command(self, command_text):

        execute_makro_tool = [{
            "type": "function",
            "function": {
                "name": "execute_makro",
                "description": "Rozpoznaje intencje i wybiera makro do wykonania",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "makro_name": {
                            "type": "string",
                            "description": "Nazwa makra w formacie snake_case"
                        }
                    },
                    "required": ["makro_name"]
                }
            }
        }]

        makros_context = json.dumps(self.available_makros, indent=2, ensure_ascii=False)

        messages=[
            {
                "role":"system",
                "content":(
                    "Jesteś inteligentnym asystentem głosowym sterującym komputerem. "
                        "Twoim zadaniem jest dopasowanie potocznego polecenia użytkownika do jednego z gotowych makr.\n\n"
                        f"Oto lista dostępnych makr i ich opisy:\n{makros_context}\n\n"
                        "Przeanalizuj polecenie i wywołaj narzędzie 'execute_makro' podając dokładną nazwę."
                )
            },
            {
                "role":"user",
                "content":command_text
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=execute_makro_tool,
                tool_choice={"type":"function","function":{"name":"execute_makro"}},
                temperature=0.1,
            )

            message = response.choices[0].message

            if message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "execute_makro":
                        args = json.loads(tool_call.function.arguments)
                        makro_name = args["makro_name"]
                        if makro_name in self.available_makros:
                            print(f"wybrano makro: {makro_name}")
                            MacroManager.run_script(makro_name, command_text)
                        else:
                            print("nie ma odpowiadajacego makra")
        except Exception as e:
            print(f"Blad komunikacji {e}")
