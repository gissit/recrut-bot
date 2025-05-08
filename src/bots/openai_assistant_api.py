import asyncio

from openai import OpenAI


class OpenAIAssistantAPI:
    __openai_client: OpenAI = None
    __assistant_id: str = ""
    __thread_id: str = ""

    __persona: str = ""

    def __init__(
        self,
        openai_model: str, openai_api_key: str, temperature: int,
        persona: str, prompt_file_path: str, initial_context: str
    ):
        self.__persona = persona

        self.__openai_client = OpenAI(api_key=openai_api_key)

        with open(prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        assistant = self.__openai_client.beta.assistants.create(
            name="RecrutBot",
            instructions=system,
            model=openai_model,
            temperature=temperature
        )
        self.__assistant_id = assistant.id

        thread = self.__openai_client.beta.threads.create(
            messages=[
                {"role": "user", "content": initial_context}
            ]
        )
        self.__thread_id = thread.id

    async def answer_to(self, message: str):
        self.__openai_client.beta.threads.messages.create(
            thread_id=self.__thread_id,
            role="user",
            content=message
        )

        run = self.__openai_client.beta.threads.runs.create(
            thread_id=self.__thread_id,
            assistant_id=self.__assistant_id
        )

        while True:
            run = self.__openai_client.beta.threads.runs.retrieve(thread_id=self.__thread_id, run_id=run.id)

            if run.status == "completed":
                break
            elif run.status in ("failed", "cancelled", "expired"):
                raise Exception(f"Assistant run failed: {run.status}")

            await asyncio.sleep(1)

        messages = self.__openai_client.beta.threads.messages.list(thread_id=self.__thread_id)
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]

        if not assistant_messages:
            return f"\n{self.__persona}[No assistant response]"

        latest_response = assistant_messages[0].content[0].text.value.strip()

        return f"\n{self.__persona}{latest_response}"

    def clean_resources(self):
        self.__openai_client.beta.assistants.delete(self.__assistant_id)
