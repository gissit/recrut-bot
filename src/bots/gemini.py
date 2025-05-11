import google.generativeai as genai

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class Gemini:
    __service: genai.ChatSession | None = None
    __model: str | None = None
    __history: list[dict[str, str | list[str]]] = []
    __initial_context: str | None = None

    __persona: str | None = None
    __temperature: float = 0.0

    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        self.__initial_context = model_configuration.initial_context
        genai.configure(api_key=model_configuration.api_key)
        self.__model = model_configuration.model
        self.__temperature = model_configuration.temperature

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        assert self.__model is not None
        assert self.__initial_context is not None

        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            {"role": "user", "parts": [system]},
            {"role": "user", "parts": [self.__initial_context]}
        ]

        gemini_model = genai.GenerativeModel(model_name=self.__model)

        self.__service = gemini_model.start_chat(history=self.__history)

        return self

    async def answer_to(self, message: str):
        response = self.__service.send_message(
            message,
            generation_config={"temperature": self.__temperature}
        )
        answer = response.text.strip()

        return f"\nGEMINI {self.__persona}{answer}"
