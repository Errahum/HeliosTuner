import os
from typing import Optional

class Config:
    TEMP_DIR = os.path.join(os.getcwd(), 'temp_files')
    def __init__(self, env_file: str = '.env'):
        self.training_data_path = ""
        self.model = "gpt-3.5-turbo"
        self.name = "fine_tuning"
        self.seed = 42
        self.n_epochs = 10
        self.learning_rate = 0.001
        self.batch_size = 32
        self.env_file = env_file
        self.openai = {
            "api_key": self._get_env_var("OPENAI_API_KEY"),
            "endpoints": {
                "chat_completion": {
                    "url": self._get_env_var("OPENAI_CHAT_COMPLETION_URL", "https://api.openai.com/v1/chat/completions"),
                    "param_label": self._get_env_var("OPENAI_CHAT_COMPLETION_PARAM_LABEL", "messages")
                },
                "fine_tuning": {
                    "url": self._get_env_var("OPENAI_FINE_TUNING_URL", "https://api.openai.com/v1/fine_tuning/jobs"),
                    "param_label": self._get_env_var("OPENAI_FINE_TUNING_PARAM_LABEL", "params")
                }
            }
        }

    def _get_env_var(self, var_name: str, default: Optional[str] = None) -> str:
        value = os.getenv(var_name, default)
        if value is None:
            raise ValueError(f"La variable d'environnement {var_name} est manquante et aucune valeur par défaut n'a été fournie.")
        return value

    def get_api_key(self) -> str:
        return self.openai["api_key"]

    def get_endpoint(self, service_type: str, model: Optional[str] = None) -> str:
        if service_type in self.openai["endpoints"]:
            return self.openai["endpoints"][service_type]["url"]
        else:
            raise ValueError(f"Type de service inconnu: {service_type}")

    def get_param_label(self, service_type: str) -> str:
        if service_type in self.openai["endpoints"]:
            return self.openai["endpoints"][service_type]["param_label"]
        else:
            raise ValueError(f"Type de service inconnu: {service_type}")

