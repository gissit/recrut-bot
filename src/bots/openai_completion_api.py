from typing import Optional
from openai import OpenAI

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class OpenAICompletionAPI:
    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__persona: Optional[str] = None
        self.__history: list[dict[str, str]] = []

        self.__initial_context = model_configuration.initial_context
        self.__temperature = model_configuration.temperature

        self.__service = OpenAI(api_key=model_configuration.api_key)
        self.__model = model_configuration.model

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            {"role": "system", "content": system},
            {"role": "user", "content": self.__initial_context}
        ]

        return self

    async def answer_to(self, message: str):
        self.__history.append({"role": "user", "content": message})

        response = self.__service.chat.completions.create(
            model=self.__model, temperature=self.__temperature, messages=self.__history
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\nOPENAI COMPLETION {self.__persona}{answer}"
