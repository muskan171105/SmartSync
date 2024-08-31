# Project Structure
```
DriveSyncApp/
│
├── credentials.json       # Google API credentials file
├── token.pickle           # Token file generated after authentication
├── main.py                # Main script to start the application
├── auth.py                # Authentication logic
├── sync.py                # Sync logic and file monitoring
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

# Syncmate

Syncmate is a desktop application that automatically syncs files from a local folder to a Google Drive account. It provides user-friendly features like Google account authentication, continuous monitoring of a specific folder, and real-time syncing of new, modified, or deleted files between the local folder and Google Drive.

## Features

- **User Authentication:** Secure login via Google account.
- **Account Selection:** Choose which Google Drive account to sync during initial setup.
- **Continuous Monitoring:** Watches a specific local folder for any changes.
- **File Syncing:** Automatically syncs new, modified, or deleted files between the local folder and Google Drive.
- **User-Friendly GUI:** Easy-to-use interface for configuration and status monitoring.

## Installation

### Prerequisites

- Python 3.6+
- Google API credentials (OAuth 2.0 client ID)

### Clone the Repository

```
git clone https://github.com/muskan171105/SmartSync.git
cd Syncmate
```

### Install Dependencies

Create a virtual environment and install the required Python packages:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Drive API for your project.
4. Create OAuth 2.0 credentials (client ID and client secret).
5. Download the credentials file (`credentials.json`) and place it in the project root directory.

### Running the Application

1. **Set Up the Local Folder Path:**

   Open `main.py` and specify the local folder path you want to monitor:
   
   ```
   local_folder = r'C:\Users\muskan srivastav\Desktop\MUSKAN\BCN'  # Update this path
   ```

2. **Run the Application:**

   ```
   python main.py
   ```

   The application will authenticate with Google and start monitoring the specified local folder for changes.

## Usage

- After running the application, sign in with your Google account.
- The application will create a folder named `DriveSyncApp` in your Google Drive.
- Any new, modified, or deleted files in the specified local folder will be automatically synced with this folder in Google Drive.


