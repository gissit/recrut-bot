"""
Manages configuration models
"""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class IaConfiguration(BaseSettings):
    gemini_model: str = Field(alias="geminiModel", default="")
    openai_model: str = Field(alias="openAiModel", default="")
    temperature: float = Field(alias="temperature", default=1.0)

    openai_api_key: str = Field(alias="OPENAI_API_KEY", default="")
    gemini_api_key: str = Field(alias="GEMINI_API_KEY", default="")

    class Config:
        populate_by_name = False
        extra = "ignore"
        env_file = ".env"


class PersonaConfiguration(BaseModel):
    recruiter: str = Field(alias="recruiter", default="")
    recruiter_context_file: str = Field(alias="recruiterContextFile", default="")
    recruiter_prompt_file: str = Field(alias="recruiterPromptFile", default="")
    candidate: str = Field(alias="candidate", default="")
    candidate_context_file: str = Field(alias="candidateContextFile", default="")
    candidate_prompt_file: str = Field(alias="candidatePromptFile", default="")

    class Config:
        populate_by_name = False
        extra = "forbid"


class PromptConfiguration(BaseModel):
    initial: str = Field(alias="initial", default="")
    recruiter_start: str = Field(alias="recruiterStart", default="")
    recruiter_end: str = Field(alias="recruiterEnd", default="")
    candidate_end: str = Field(alias="candidateEnd", default="")

    class Config:
        populate_by_name = False
        extra = "forbid"


class AppConfiguration(BaseModel):
    ia: IaConfiguration
    persona: PersonaConfiguration
    prompt: PromptConfiguration

    class Config:
        populate_by_name = False
        extra = "forbid"
