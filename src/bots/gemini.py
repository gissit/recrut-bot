import google.generativeai as genai

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class Gemini:
    __gemini_chat_session: genai.ChatSession | None = None
    __gemini_model: str | None = None
    __temperature: int = 0.0

    __persona: str | None = None
    __history: list = []

    def __init__(
        self,
        model_configuration: BotModelConfiguration
    ):
        genai.configure(api_key=model_configuration.api_key)
        self.__gemini_model = model_configuration.model
        self.__temperature = model_configuration.temperature

        self.__history = [
            {"role": "user", "parts": [model_configuration.initial_context]}
        ]

    def set_persona(self, persona_configuration: BotPersonaConfiguration):
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history.insert(0, {"role": "user", "parts": [system]})

        gmodel = genai.GenerativeModel(model_name=self.__gemini_model)

        self.__gemini_chat_session = gmodel.start_chat(history=self.__history)

        return self

    async def answer_to(self, message):
        response = self.__gemini_chat_session.send_message(
            message,
            generation_config={"temperature": self.__temperature}
        )
        answer = response.text.strip()

        return f"\nGEMINI {self.__persona}{answer}"
