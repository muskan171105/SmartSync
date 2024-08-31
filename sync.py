import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from auth import authenticate
from googleapiclient.http import MediaFileUpload

class SyncHandler(FileSystemEventHandler):
    def __init__(self, service, folder_id):
        self.service = service
        self.folder_id = folder_id
        self.last_modified = {}

    def upload_file(self, file_path):
        try:
            print(f"Uploading file: {file_path}")
            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [self.folder_id]
            }
            media = MediaFileUpload(file_path, resumable=True)
            self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"File uploaded: {file_path}")
        except PermissionError:
            print(f"Permission error uploading file: {file_path}. Retrying in 5 seconds...")
            time.sleep(5)
            self.upload_file(file_path)
        except Exception as e:
            print(f"Error uploading file: {file_path} - {e}")

    def delete_file(self, file_name):
        try:
            print(f"Deleting file: {file_name}")
            results = self.service.files().list(q=f"name='{file_name}' and '{self.folder_id}' in parents").execute()
            items = results.get('files', [])
            if items:
                for item in items:
                    self.service.files().delete(fileId=item['id']).execute()
                    print(f"File deleted: {file_name}")
        except Exception as e:
            print(f"Error deleting file: {file_name} - {e}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.upload_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.upload_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            self.delete_file(os.path.basename(event.src_path))

def start_monitoring(local_folder, service, folder_id):
    # Sync existing files in the local folder
    sync_existing_files(local_folder, service, folder_id)

    # Start the observer to watch for changes
    event_handler = SyncHandler(service, folder_id)
    observer = Observer()
    observer.schedule(event_handler, path=local_folder, recursive=True)
    observer.start()
    print(f"Monitoring folder: {local_folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def sync_existing_files(local_folder, service, folder_id):
    print("Syncing existing files...")
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            print(f"Checking file: {file_name}")

            # Check if file already exists in Google Drive
            results = service.files().list(q=f"name='{file_name}' and '{folder_id}' in parents").execute()
            items = results.get('files', [])

            if not items:
                print(f"Uploading file: {file_path}")
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(file_path, resumable=True)
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print(f"File uploaded: {file_path}")
            else:
                print(f"File already exists: {file_name}")
    print("Existing files synced.")
