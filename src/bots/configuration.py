

class BotModelConfiguration:
    def __init__(self, model: str, api_key: str, temperature: float, initial_context: str):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.initial_context = initial_context


class BotPersonaConfiguration:
    def __init__(self, persona: str, prompt_file_path: str):
        self.persona = persona
        self.prompt_file_path = prompt_file_path
