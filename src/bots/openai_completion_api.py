from openai import OpenAI

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class OpenAICompletionAPI:
    __openai_client: OpenAI | None = None
    __openai_model: str | None = None
    __temperature: float = 0.0

    __persona: str | None = None
    __history: list[dict[str, str]] = []

    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__openai_client = OpenAI(api_key=model_configuration.api_key)
        self.__openai_model = model_configuration.model
        self.__temperature = model_configuration.temperature

        self.__history = [
            {"role": "user", "content": model_configuration.initial_context}
        ]

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history.insert(0, {"role": "system", "content": system})

        return self

    async def answer_to(self, message: str):
        assert self.__openai_client is not None
        assert self.__openai_model is not None

        self.__history.append({"role": "user", "content": message})

        response = self.__openai_client.chat.completions.create(
            model=self.__openai_model, temperature=self.__temperature, messages=self.__history
        )
        answer = response.choices[0].message.content.strip()

        self.__history.append(response.choices[0].message)

        return f"\nOPENAI COMPLETION {self.__persona}{answer}"
