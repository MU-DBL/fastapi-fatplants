import yaml
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("place") == 'docker'and os.getenv("APP_ENV") == 'prod':
    path = "/app/fatplants_volume/config.yaml"
elif os.getenv("place") == 'docker':
    path = "/app/fatplants_volume/config-dev.yaml"
else:
     raise ValueError('Environment variable "place" is not set to "docker".')

try:
    with open(path) as file:
        yaml_file = yaml.load(file, Loader=yaml.FullLoader)
        db = yaml_file["database"]
        open_api=yaml_file["open-api"]
        gmail_api = yaml_file["gmail-api"]

except FileNotFoundError:
    raise FileNotFoundError(f"Could not open the file at {path + 'config.yaml'}. Please check the path and file existence.")
except IOError as e:
    raise IOError(f"An I/O error occurred while trying to open the file at {path + 'config.yaml'}: {str(e)}")

db_credentials = db
open_api_credentials=open_api
gmail_api_credentials=gmail_api