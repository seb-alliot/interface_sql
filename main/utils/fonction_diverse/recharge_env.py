from dotenv import load_dotenv
import os
import sys

def recharger_env(env_path=None):
    env_path = env_path or os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path, override=True)
