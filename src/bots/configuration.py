

class BotModelConfiguration:
    def __init__(self, model, api_key, temperature, initial_context):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.initial_context = initial_context


class BotPersonaConfiguration:
    def __init__(self, persona, prompt_file_path):
        self.persona = persona
        self.prompt_file_path = prompt_file_path
