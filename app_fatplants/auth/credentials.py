import yaml
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("place") == "docker":
    path = "/app/"
else:
    path = "/home/scd2z/fatplants/fastapi-fatplants/app_fatplants/"


with open(path + "config.yaml") as file:
    yaml_file = yaml.load(file, Loader=yaml.FullLoader)
    db = yaml_file["database"]
    open_api=yaml_file["open-api"]
    gmail_api = yaml_file["gmail-api"]


db_credentials = db
open_api_credentials=open_api
gmail_api_credentials=gmail_api