"""
Manages configuration

Configuration is explicitly declared as classes with near-to-empty attributes
in order to ease development with auto-completion discovery.
"""

import json
import os

from .configuration_models import AppConfiguration

# working directory is repository root directory
WORKING_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

config_file_path = os.path.join(WORKING_DIRECTORY, "src/config.json")

with open(config_file_path, "r", encoding="utf-8") as f:
    config_data = json.load(f)

Configuration = AppConfiguration.model_validate(config_data)
