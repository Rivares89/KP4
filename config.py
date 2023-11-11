from decouple import AutoConfig

config = AutoConfig()
API_KEY=config("API_KEY")