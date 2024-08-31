import os
from auth import authenticate
from sync import start_monitoring

def main():
    local_folder = os.path.expanduser(r'C:\Users\muskan srivastav\Desktop\MUSKAN\BCN')
    service = authenticate()

    # Check if the Google Drive folder exists, otherwise create it
    folder_metadata = {
        'name': 'DriveSyncApp',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder_id = None
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder' and name='DriveSyncApp'").execute()
    items = results.get('files', [])
    if items:
        folder_id = items[0]['id']
    else:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')

    # Start monitoring the local folder
    start_monitoring(local_folder, service, folder_id)

if __name__ == '__main__':
    main()
