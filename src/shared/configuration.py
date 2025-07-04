import json
import os

from .configuration_models import AppConfiguration

# working directory is repository root directory
WORKING_DIRECTORY: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

APP_NAME: str = "RecrutBot"

config_file_path = os.path.join(WORKING_DIRECTORY, "src/config.json")

with open(config_file_path, "r", encoding="utf-8") as f:
    config_data = json.load(f)

Configuration = AppConfiguration.model_validate(config_data)
