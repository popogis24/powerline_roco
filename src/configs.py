import tomli as toml

class Config:
    def __init__(self, filepath=r"C:\taesa\powerline_roco\settings.toml"):
        with open(filepath, "rb") as file:  # Open the file in binary mode
            self.settings = toml.load(file)

    def __getattr__(self, name):
        return self.settings.get(name, None)
