This is a proper project of mine, so I'll have actual documentation for this.

# What is this and what does it do

These 2 files were created by me to automatically upload scanned documents to google drive and hyperlink them within google sheets.
Theoretically it should work with any file type but I just used .jpg/.jpeg (you may need to change the code in line 18 of the hyperlinking file)

# How do I use this?

Good question. First install python, I used version 3.12 personally but it should work with any recent version of python. Then install the necessary libraries with running "pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog" in terminal.

Then you need to go to google cloud and make an account if you do not already have one. Create a new project or use the one labeled "My first project". Navigate to "IAM & Admin" then go to "service accounts". Click "create service account", give it a name and ID, then click continue. When giving a role, grant it the role of owner and continue and hit done. Now you need to click on your new service account, go to keys, and create a new key (JSON). It will automatically download the key and you need to replace "your_credentials.json" with the path of this JSON file in both python files. The last thing you need to do in google cloud is head to "API's and services" and enable the Google drive API and Google Sheets API.

Assuming you already have a google folder and spreadsheet setup, grab their ids by opening them and looking at it's url. For example; a google folder's ID will be "aowiudhj9231hu123as" from the URL "drive.google.com/drive/u/0/folders/aowiudhj9231hu123as", and it'll work the same way for the spreadsheet. Make sure to put in both of these IDs into the file (both files need the drive folder ID but only the hyperlink file needs the spreadsheet ID). Also remember to enter your local folder's path that you're monitoring into the "constantly scans" file.

 It is also important to share both the google folder and google spreadsheet to your service account's email. (ENABLE EDITING PERMISSIONS)

# You're done!

Now you just need to keep the "constantly scans" file open at all times, and use the second "hyperlink" file once you're done to hyperlink everything (you can customize what sheet, row, column, and starting cell to hyperlink by editing the "hyperlink" file)

Contact me by opening an issue, and feel free to build upon my work! (I would appreciate crediting me though)
