import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Replace 'your_credentials.json' with the path to your Google service account credentials JSON file
credentials_path = 'your_credentials.json'

drive_service = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive']))
# replace your_local_folder_path with the path to the folder you want to monitor
local_folder_path = 'your_local_folder_path'

drive_folder_id = 'your_drive_folder_id' #replace your_drive_folder_id with the ID of the Google Drive folder you want to upload to
    #must be shared to service account email

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        time.sleep(2)
        print(f"New file created: {file_path}")
        upload_to_drive(file_path)

def upload_to_drive(file_path):
    try:
        file_metadata = {'name': os.path.basename(file_path), 'parents': [drive_folder_id]}
        media = drive_service.files().create(body=file_metadata, media_body=file_path).execute()
        print(f"File uploaded to Google Drive: {media['name']}")
    except Exception as e:
        print(f"Error uploading file to Google Drive: {e}")
        
if __name__ == "__main__":
    # important
    event_handler = FileHandler()

    observer = Observer()
    observer.schedule(event_handler, path=local_folder_path, recursive=False)

    print(f"Monitoring local folder: {local_folder_path}")
    print(f"Uploading to Google Drive folder with ID: {drive_folder_id}")
    print("Press Ctrl+C to stop monitoring.")

    try:
        
        observer.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # stops the program
        observer.stop()

    observer.join()

