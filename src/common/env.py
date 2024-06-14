import os
import environ
from pathlib import Path

# Initiate related env class
env = environ.Env()

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '../../.env'))
