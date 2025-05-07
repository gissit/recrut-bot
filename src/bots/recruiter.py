import google.generativeai as genai


class Recruiter():
    __gemini_chat_session: genai.ChatSession = None

    __temperature: int = 0.0
    __persona: str = ""

    def __init__(
        self,
        gemini_model: str, gemini_api_key: str, temperature: int,
        persona: str, prompt_file_path: str, initial_context: str
    ):
        self.__temperature = temperature
        self.__persona = persona

        with open(prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        history = [
            {"role": "user", "parts": [system]},
            {"role": "user", "parts": initial_context}
        ]

        genai.configure(api_key=gemini_api_key)
        gmodel = genai.GenerativeModel(gemini_model)

        self.__gemini_chat_session = gmodel.start_chat(history=history)

    async def answer_to(self, message):
        response = self.__gemini_chat_session.send_message(
            message,
            generation_config={"temperature": self.__temperature}
        ).text.strip()

        return f"\n{self.__persona}{response}"
