from dataclasses import dataclass


@dataclass
class BotModelConfiguration:
    model: str
    api_key: str
    temperature: float
    initial_context: str

    def __post_init__(self):
        if not self.model:
            raise ValueError("model must not be empty")
        if not self.api_key:
            raise ValueError("api_key must not be empty")
        if not self.initial_context:
            raise ValueError("initial_context must not be None")
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError("temperature must be between 0 and 2")


@dataclass
class BotPersonaConfiguration:
    persona: str
    prompt_file_path: str

    def __post_init__(self):
        if not self.persona:
            raise ValueError("persona must not be empty")
        if not self.prompt_file_path:
            raise ValueError("prompt_file_path must not be empty")
