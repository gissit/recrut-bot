import google.generativeai as genai


class Recruiter():
    __gemini_chat_session: genai.ChatSession = None
    __gemini_model: str = ""
    __gemini_api_key: str = ""

    __temperature: int = 0.0
    __persona: str = ""

    def __init__(
        self,
        gemini_model: str, gemini_api_key: str, temperature: int,
        persona: str, prompt_file_path: str, initial_context: str
    ):
        self.__gemini_model = gemini_model
        self.__gemini_api_key = gemini_api_key
        self.__temperature = temperature
        self.__persona = persona

        with open(prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        history = [
            {"role": "user", "parts": [system]},
            {"role": "user", "parts": initial_context}
        ]

        genai.configure(api_key=self.__gemini_api_key)
        gmodel = genai.GenerativeModel(self.__gemini_model)

        self.__gemini_chat_session = gmodel.start_chat(history=history)

    async def ask(self, message):
        response = self.__gemini_chat_session.send_message(
            message,
            generation_config={"temperature": self.__temperature}
        ).text.strip()

        print(f"\n{self.__persona}{response}")

        return response
