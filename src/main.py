import argparse
import os
import asyncio

from shared import (
    FileContext,
    Configuration,
    WORKING_DIRECTORY,
    APP_NAME
)
from bots import (
    BotModelConfiguration,
    BotPersonaConfiguration,
    Gemini,
    OpenAICompletionAPI,
    OpenAIAssistantAPI,
    MistralCompletion
)


class Main:
    __bots: dict[str, Gemini | OpenAICompletionAPI | OpenAIAssistantAPI | MistralCompletion] = {}
    __recruiter: Gemini | OpenAICompletionAPI | OpenAIAssistantAPI | MistralCompletion
    __candidate: Gemini | OpenAICompletionAPI | OpenAIAssistantAPI | MistralCompletion

    def __init__(self):
        file_contexts = {
            "POSTE_CONTEXT": FileContext(
                os.path.join(
                    WORKING_DIRECTORY,
                    Configuration.persona.recruiter_context_file
                )
            ).get_context(),
            "CV_CONTEXT": FileContext(
                os.path.join(
                    WORKING_DIRECTORY,
                    Configuration.persona.candidate_context_file
                )
            ).get_context()
        }
        initial_context = Configuration.prompt.initial.format_map(file_contexts)

        gemini_configuration = BotModelConfiguration(
            Configuration.ia.gemini_model,
            Configuration.ia.gemini_api_key,
            Configuration.ia.temperature,
            initial_context
        )
        mistral_configuration = BotModelConfiguration(
            Configuration.ia.mistral_model,
            Configuration.ia.mistral_api_key,
            Configuration.ia.temperature,
            initial_context
        )
        openai_configuration = BotModelConfiguration(
            Configuration.ia.openai_model,
            Configuration.ia.openai_api_key,
            Configuration.ia.temperature,
            initial_context
        )

        self.__bots = {
            "gemini": Gemini(gemini_configuration),
            "mistral": MistralCompletion(mistral_configuration),
            "openai_completion": OpenAICompletionAPI(openai_configuration),
            "openai_assistant": OpenAIAssistantAPI(openai_configuration)
        }

    def __setup_interview(self):
        recruiter_persona = BotPersonaConfiguration(
            Configuration.persona.recruiter_prefix,
            os.path.join(WORKING_DIRECTORY, Configuration.persona.recruiter_prompt_file)
        )
        self.__recruiter = self.__bots[Configuration.persona.recruiter].set_persona(recruiter_persona)

        candidate_persona = BotPersonaConfiguration(
            Configuration.persona.candidate_prefix,
            os.path.join(WORKING_DIRECTORY, Configuration.persona.candidate_prompt_file)
        )
        self.__candidate = self.__bots[Configuration.persona.candidate].set_persona(candidate_persona)

    async def start_interview(self, max_turns: int):
        self.__setup_interview()

        recruiter_response = await self.__recruiter.answer_to(Configuration.prompt.recruiter_start)
        print(recruiter_response)

        for _ in range(max_turns):
            candidate_response = await self.__candidate.answer_to(recruiter_response)
            print(candidate_response)

            recruiter_response = await self.__recruiter.answer_to(candidate_response)
            print(recruiter_response)

        recruiter_response = f"{recruiter_response}{Configuration.prompt.candidate_end}"

        candidate_response = await self.__candidate.answer_to(recruiter_response)
        print(candidate_response)

        recruiter_response = await self.__recruiter.answer_to(Configuration.prompt.recruiter_end)
        print(recruiter_response)


async def main():
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--max-turns", type=int, default=4, help="Maximum number of turns in the discussion")

    args = parser.parse_args()

    await Main().start_interview(args.max_turns)


if __name__ == "__main__":
    asyncio.run(main())
