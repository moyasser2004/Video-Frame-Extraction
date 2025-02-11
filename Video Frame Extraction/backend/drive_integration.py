from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

class GoogleDriveIntegration:
    def __init__(self, credentials_file="credentials.json"):
        self.credentials_file = credentials_file
        self.service = self.authenticate_google_drive()

    def authenticate_google_drive(self):
        """Authenticate and connect to Google Drive."""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/drive"]
        )
        return build("drive", "v3", credentials=credentials)

    def upload_to_drive(self, file_path, folder_id):
        """
        Upload a file to Google Drive.
        :param file_path: Path to the file to upload.
        :param folder_id: ID of the folder to upload to.
        :return: ID of the uploaded file.
        """
        file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")