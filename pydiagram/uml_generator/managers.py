import copy
import json


class ElementConfigManager:
    _instance = None

    def __new__(cls, file_path: object = None) -> object:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = None
            if file_path:
                cls._instance.load_config(file_path)
            else:
                print("Warning: No file path provided. Configuration will be empty.")
        return cls._instance

    def load_config(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            print(f"Arquivo {file_path} não encontrado.")
            self._config = {}

    def get_config(self):
        return copy.deepcopy(self._config)

    def set_config(self, key, value, file_path):
        self._config[key] = value
        with open(file_path, 'w') as f:
            json.dump(self._config, f, indent=4)

    @staticmethod
    def get_manager():
        return ElementConfigManager._instance
