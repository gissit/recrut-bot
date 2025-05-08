from bots.configuration import BotModelConfiguration, BotPersonaConfiguration


def test_bot_model_configuration_initialization():
    config = BotModelConfiguration(
        model="gpt-4",
        api_key="test-key",
        temperature=0.7,
        initial_context="Hello, world!"
    )
    assert config.model == "gpt-4"
    assert config.api_key == "test-key"
    assert config.temperature == 0.7
    assert config.initial_context == "Hello, world!"


def test_bot_persona_configuration_initialization():
    persona = BotPersonaConfiguration(
        persona="recruiter",
        prompt_file_path="prompts/recruiter.txt"
    )
    assert persona.persona == "recruiter"
    assert persona.prompt_file_path == "prompts/recruiter.txt"
