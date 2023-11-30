from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import time


# Replace 'your_credentials.json' with the path to your Google service account credentials JSON file
credentials_path = 'your_credentials.json'
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])


# Google Drive API setup
drive_service = build('drive', 'v3', credentials=credentials)


# Google Sheets API setup
sheets_service = build('sheets', 'v4', credentials=credentials)


# Folder where the image will be uploaded
folder_id = 'your_folder_id'


# Google Spreadsheet ID
spreadsheet_id = 'your_spreadsheet_id'


def upload_image_and_link(file_path):
    # Upload image to Google Drive
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = drive_service.files().create(body=file_metadata, media_body=file_path).execute()


    # Wait for the file to be processed by Google Drive
    time.sleep(5)


    # Get the image file ID
    image_file_id = media['id']


    # Get the current sheet values
    sheet = sheets_service.spreadsheets()
    sheet_values = sheet.values().get(spreadsheetId=spreadsheet_id, range='Sheet1').execute()
    values = sheet_values.get('values', [])


    # Add a new row with the image hyperlink
    new_row = [f'=HYPERLINK("https://drive.google.com/file/d/{image_file_id}", "View Image")']
    values.append(new_row)


    # Update the sheet with the new values
    sheet.values().update(spreadsheetId=spreadsheet_id, range='Sheet1', body={'values': values}, valueInputOption='RAW').execute()


# Example usage
image_path = 'path/to/your/image.jpg'
upload_image_and_link(image_path)