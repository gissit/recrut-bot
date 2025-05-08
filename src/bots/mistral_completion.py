from mistralai import Mistral

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class MistralCompletion:
    __mistral_client: Mistral | None = None
    __mistral_model: str | None = None

    __temperature: float = 0.0
    __persona: str | None = None
    __history: list = []

    def __init__(
        self,
        model_configuration: BotModelConfiguration,
        persona_configuration: BotPersonaConfiguration
    ):
        self.__mistral_model = model_configuration.model
        self.__temperature = model_configuration.temperature
        self.__persona = persona_configuration.persona

        self.__mistral_client = Mistral(api_key=model_configuration.api_key)

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            {"role": "system", "content": system},
            {"role": "user", "content": model_configuration.initial_context},
        ]

    async def answer_to(self, message: str):
        self.__history.append({"role": "user", "content": message})

        response = self.__mistral_client.chat.complete(
            model=self.__mistral_model,
            messages=self.__history,
            temperature=self.__temperature
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\n{self.__persona}{answer}"
