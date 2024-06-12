import os
from dotenv import load_dotenv
def import_env_var(var_name):
    load_dotenv('.env', override=True)
    env_var = os.getenv(var_name)
    if env_var is None:
        raise ValueError(f"{var_name} not found. Please check your .env file.")
    else:
        return env_var

OPENAI_API_KEY = import_env_var("OPENAI_API_KEY")