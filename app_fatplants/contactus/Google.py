import os
import json
import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime  # Don't forget to import datetime if you're using the convert_to_RFC_datetime function

def Create_Service(api_name, api_version, *scopes):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(API_SERVICE_NAME, API_VERSION, SCOPES, sep='-')

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            # Use environment variable for client secret
            # with open('/app/auth/email_client_secret.json') as json_data:
            with open('./auth/email_client_secret.json') as json_data:

                client_secret_dict = json.load(json_data)

            # client_secret_json_string = os.getenv("CONTACTUS_SFTP_CLIENT_SECRET")
            # if client_secret_json_string is None:
            #     raise ValueError("Environment variable 'CONTACTUS_SFTP_CLIENT_SECRET' not found")

            #client_secret_dict = json.loads(client_secret_json_string)
            flow = InstalledAppFlow.from_client_config(client_secret_dict, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(f'{API_SERVICE_NAME} service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
