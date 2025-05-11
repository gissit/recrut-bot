from mistralai import Messages, Mistral, SystemMessage, UserMessage

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class MistralCompletion:
    __service: Mistral | None = None
    __model: str | None = None
    __history: list[Messages] = []
    __initial_context: str | None = None

    __persona: str | None = None
    __temperature: float = 0.0

    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__initial_context = model_configuration.initial_context
        self.__service = Mistral(api_key=model_configuration.api_key)
        self.__model = model_configuration.model
        self.__temperature = model_configuration.temperature

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
        assert self.__service is not None
        assert self.__model is not None

        self.__history.append(UserMessage(content=message))

        response = self.__service.chat.complete(
            model=self.__model,
            messages=self.__history,
            temperature=self.__temperature
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\nMISTRAL {self.__persona}{answer}"
