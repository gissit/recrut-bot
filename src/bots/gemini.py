import google.generativeai as genai

from .configuration import BotModelConfiguration, BotPersonaConfiguration


class Gemini:
    __gemini_chat_session: genai.ChatSession | None = None

    __temperature: int = 0.0
    __persona: str | None = None

    def __init__(
        self,
        model_configuration: BotModelConfiguration,
        persona_configuration: BotPersonaConfiguration
    ):
        self.__temperature = model_configuration.temperature
        self.__persona = persona_configuration.persona

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        history = [
            {"role": "user", "parts": [system]},
            {"role": "user", "parts": [model_configuration.initial_context]}
        ]

        genai.configure(api_key=model_configuration.api_key)
        gmodel = genai.GenerativeModel(model_name=model_configuration.model)

        self.__gemini_chat_session = gmodel.start_chat(history=history)

    async def answer_to(self, message):
        response = self.__gemini_chat_session.send_message(
            message,
            generation_config={"temperature": self.__temperature}
        )
        answer = response.text.strip()

        return f"\n{self.__persona}{answer}"
