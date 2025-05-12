from typing import Optional
from mistralai import Messages, Mistral, SystemMessage, UserMessage

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class MistralCompletion:
    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__persona: Optional[str] = None
        self.__history: list[Messages] = []

        self.__initial_context = model_configuration.initial_context
        self.__temperature = model_configuration.temperature

        self.__service = Mistral(api_key=model_configuration.api_key)
        self.__model = model_configuration.model

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            SystemMessage(content=system),
            UserMessage(content=self.__initial_context)
        ]

        return self

    async def answer_to(self, message: str):
        self.__history.append(UserMessage(content=message))

        response = self.__service.chat.complete(
            model=self.__model,
            messages=self.__history,
            temperature=self.__temperature
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\nMISTRAL {self.__persona}{answer}"
