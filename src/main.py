"""
Holds IA contexts and RAG.
"""

import argparse
import os
import asyncio

from shared import Configuration, WORKING_DIRECTORY
from bots import FileContext, Recruiter, Candidate


class Main():
    __recruiter: Recruiter
    __candidate: Candidate

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

        self.__recruiter = Recruiter(
            Configuration.ia.gemini_model,
            Configuration.ia.gemini_api_key,
            Configuration.ia.temperature,
            Configuration.persona.recruiter,
            os.path.join(WORKING_DIRECTORY, Configuration.persona.recruiter_prompt_file),
            initial_context
        )

        self.__candidate = Candidate(
            Configuration.ia.openai_model,
            Configuration.ia.openai_api_key,
            Configuration.ia.temperature,
            Configuration.persona.candidate,
            os.path.join(WORKING_DIRECTORY, Configuration.persona.candidate_prompt_file),
            initial_context
        )

    async def duel(self, max_turns: int):
        recruiter_response = await self.__recruiter.ask(Configuration.prompt.recruiter_start)

        self.__candidate.append_message("user", recruiter_response)

        for _ in range(max_turns):
            candidate_response = await self.__candidate.ask()

            self.__recruiter.append_message(candidate_response)

            recruiter_response = await self.__recruiter.ask(candidate_response)

            self.__candidate.append_message("user", recruiter_response)

        self.__candidate.append_message("user", Configuration.prompt.candidate_end)

        candidate_response = await self.__candidate.ask()

        recruiter_response = await self.__recruiter.ask(Configuration.prompt.recruiter_end)


async def main():
    parser = argparse.ArgumentParser(description="Bullshit Bob")
    parser.add_argument("--max-turns", type=int, default=4, help="Nombre tour max")

    args = parser.parse_args()

    await Main().duel(args.max_turns)


if __name__ == "__main__":
    asyncio.run(main())
