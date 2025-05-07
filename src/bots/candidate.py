from openai import OpenAI


class Candidate():
    __openai_client: OpenAI = None
    __openai_model: str = ""

    __temperature: int = 0.0
    __persona: str = ""
    __history: list = []

    def __init__(
        self,
        openai_model: str, openai_api_key: str, temperature: int,
        persona: str, prompt_file_path: str, initial_context: str
    ):
        self.__openai_model = openai_model
        self.__temperature = temperature
        self.__persona = persona

        self.__openai_client = OpenAI(api_key=openai_api_key)

        with open(prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            {"role": "system", "content": system},
            {"role": "user", "content": initial_context}
        ]

    async def answer_to(self, message: str):
        self.__history.append({"role": "user", "content": message})

        response = self.__openai_client.chat.completions.create(
            model=self.__openai_model, temperature=self.__temperature, messages=self.__history
        ).choices[0].message.content.strip()

        self.__history.append({"role": "assistant", "content": response})

        return f"\n{self.__persona}{response}"

    def clean_resources(self):
        pass
