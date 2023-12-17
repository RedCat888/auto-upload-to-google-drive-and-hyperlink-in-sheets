import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace 'your_credentials.json' with the path to your Google service account credentials JSON file
credentials_path = 'your_credentials.json'

# Google Sheets API setup
sheets_service = build('sheets', 'v4', credentials=service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets']))

# Replace 'your_spreadsheet_id' with the actual ID of your Google Spreadsheet
spreadsheet_id = 'your_spreadsheet_id'
# Replace 'your_folder_id' with the actual ID of the Google Drive folder containing your images
folder_id = 'your_folder_id'

def get_image_urls(drive_service, folder_id):
    # Retrieve a list of files in the specified Google Drive folder
    response = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType='image/jpeg'", fields='files(id,name)').execute()
    files = response.get('files', [])

    # Generate image URLs
    image_urls = [f"https://drive.google.com/uc?id={file['id']}" for file in files]
    return image_urls

def update_sheet_with_image_urls(sheet_service, spreadsheet_id, image_urls, sheet_name='Sheet1'): #remember to change 'Sheet1' to the name of your sheet
    # Get the number of images
    num_images = len(image_urls)

    if num_images > 0:
        # Reverse the order of image_urls to link the oldest images first
        image_urls.reverse()

        # Prepare values for the sheet (direct hyperlink formulas)
        values = [[f'=HYPERLINK("{url}","Image")'] for url in image_urls]

        # Calculate the range of cells to update
        start_cell = 1 #change this to whatever cell you want to start at
        range_to_update = f'{sheet_name}!J{start_cell}:J{start_cell + num_images - 1}'

        # Update the sheet with the new values using USER_ENTERED to allow formulas
        sheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_to_update,
            body={'values': values},
            valueInputOption='USER_ENTERED'
        ).execute()
    else:
        print("No images to update in the sheet.")

if __name__ == "__main__":
    # Google Drive API setup
    drive_service = build('drive', 'v3', credentials=service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://www.googleapis.com/auth/drive']))

    # Get image URLs from the specified Google Drive folder
    image_urls = get_image_urls(drive_service, folder_id)

    # Update the Google Sheet with hyperlinks to the images
    update_sheet_with_image_urls(sheets_service, spreadsheet_id, image_urls)

    print(f"Hyperlinked images added to the Google Sheet: {spreadsheet_id}")
