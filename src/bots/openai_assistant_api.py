import asyncio
import signal
import atexit

from openai import OpenAI
from .configuration import BotModelConfiguration, BotPersonaConfiguration


class OpenAIAssistantAPI:
    __openai_client: OpenAI | None = None
    __assistant_id: str | None = None
    __thread_id: str | None = None

    __persona: str | None = None

    def __init__(
        self,
        model_configuration: BotModelConfiguration,
        persona_configuration: BotPersonaConfiguration
    ):
        atexit.register(self._delete_assistant)
        signal.signal(signal.SIGINT, self._delete_assistant)
        signal.signal(signal.SIGTERM, self._delete_assistant)

        self.__persona = persona_configuration.persona

        self.__openai_client = OpenAI(api_key=model_configuration.api_key)

        with open(persona_configuration.prompt_file_path, encoding="utf-8") as f:
            system = f.read()

        assistant = self.__openai_client.beta.assistants.create(
            name="RecrutBot",
            instructions=system,
            model=model_configuration.model,
            temperature=model_configuration.temperature,
        )
        self.__assistant_id = assistant.id

        thread = self.__openai_client.beta.threads.create(
            messages=[
                {"role": "user", "content": model_configuration.initial_context}
            ]
        )
        self.__thread_id = thread.id

    def _delete_assistant(self):
        self.__openai_client.beta.assistants.delete(self.__assistant_id)

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

        answer = assistant_messages[0].content[0].text.value.strip()

        return f"\nOPENAI ASSISTANT {self.__persona}{answer}"
