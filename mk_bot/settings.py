import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
dotenv_path = join(parent_dir, '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")