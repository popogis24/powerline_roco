import os
import tomllib as toml

class Config:
    def __init__(self, filepath="path_to_your_toml_file.toml"):
        with open(filepath, "rb") as file:  # Open the file in binary mode
            self.settings = toml.load(file)

    def __getattr__(self, name):
        return self.settings.get(name, None)
