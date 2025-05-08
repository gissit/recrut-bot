from mistralai import Mistral


class MistralCompletion:
    __mistral_client: Mistral = None
    __mistral_model: str = ""

    __temperature: float = 0.0
    __persona: str = ""
    __history: list = []

    def __init__(
        self,
        mistral_model: str,
        mistral_api_key: str,
        temperature: float,
        persona: str,
        prompt_file_path: str,
        initial_context: str
    ):
        self.__mistral_model = mistral_model
        self.__temperature = temperature
        self.__persona = persona

        self.__mistral_client = Mistral(api_key=mistral_api_key)

        with open(prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        self.__history = [
            {"role": "system", "content": system},
            {"role": "user", "content": initial_context}
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

    def clean_resources(self):
        pass
