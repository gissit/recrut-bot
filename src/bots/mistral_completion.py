from mistralai import Messages, Mistral, SystemMessage, UserMessage

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class MistralCompletion:
    __mistral_client: Mistral | None = None
    __mistral_model: str | None = None
    __temperature: float = 0.0

    __persona: str | None = None
    __history: list[Messages] = []

    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__mistral_client = Mistral(api_key=model_configuration.api_key)
        self.__mistral_model = model_configuration.model
        self.__temperature = model_configuration.temperature

        self.__history = [
            UserMessage(content=model_configuration.initial_context)
        ]

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history.insert(0, SystemMessage(content=system))

        return self

    async def answer_to(self, message: str):
        assert self.__mistral_client is not None
        assert self.__mistral_model is not None

        self.__history.append(UserMessage(content=message))

        response = self.__mistral_client.chat.complete(
            model=self.__mistral_model,
            messages=self.__history,
            temperature=self.__temperature
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\nMISTRAL {self.__persona}{answer}"
