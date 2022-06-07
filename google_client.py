from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_files_client():
    creds = service_account.Credentials.from_service_account_file(
        "deep-tracer-352516-60b84781d276.json", scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    files_api_client = service.files()
    return files_api_client
