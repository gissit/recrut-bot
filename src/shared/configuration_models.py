from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class IaConfiguration(BaseSettings):
    model_config = SettingsConfigDict(
        populate_by_name=False,
        extra="ignore",
        env_file=".env"
    )

    gemini_model: str = Field(alias="geminiModel", default="")
    openai_model: str = Field(alias="openAiModel", default="")
    mistral_model: str = Field(alias="mistralModel", default="")
    temperature: float = Field(alias="temperature", default=1.0)

    openai_api_key: str = Field(alias="OPENAI_API_KEY", default="")
    gemini_api_key: str = Field(alias="GEMINI_API_KEY", default="")
    mistral_api_key: str = Field(alias="MISTRAL_API_KEY", default="")


class PersonaConfiguration(BaseModel):
    model_config = ConfigDict(
        populate_by_name=False,
        extra="forbid"
    )

    recruiter: str = Field(alias="recruiter", default="")
    recruiter_prefix: str = Field(alias="recruiterPrefix", default="")
    recruiter_context_file: str = Field(alias="recruiterContextFile", default="")
    recruiter_prompt_file: str = Field(alias="recruiterPromptFile", default="")
    candidate: str = Field(alias="candidate", default="")
    candidate_prefix: str = Field(alias="candidatePrefix", default="")
    candidate_context_file: str = Field(alias="candidateContextFile", default="")
    candidate_prompt_file: str = Field(alias="candidatePromptFile", default="")


class PromptConfiguration(BaseModel):
    model_config = ConfigDict(
        populate_by_name=False,
        extra="forbid"
    )

    initial: str = Field(alias="initial", default="")
    recruiter_start: str = Field(alias="recruiterStart", default="")
    recruiter_end: str = Field(alias="recruiterEnd", default="")
    candidate_end: str = Field(alias="candidateEnd", default="")


class AppConfiguration(BaseModel):
    model_config = ConfigDict(
        populate_by_name=False,
        extra="forbid"
    )

    ia: IaConfiguration
    persona: PersonaConfiguration
    prompt: PromptConfiguration
