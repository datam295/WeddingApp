from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def run():
    print('Checking spreadsheet metadata using service account')
    print('cwd:', os.getcwd())
    print('service account exists:', os.path.exists(SERVICE_ACCOUNT_FILE))
    
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    spreadsheet_id = os.getenv('WEDDING_SHEET_ID', 'your-spreadsheet-id-here')
    print('Spreadsheet ID:', spreadsheet_id)

    try:
        # Call spreadsheets.get to fetch metadata
        resp = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        print('Metadata retrieved:')
        print('Title:', resp.get('properties', {}).get('title'))
        print('Sheets:', [s.get('properties', {}).get('title') for s in resp.get('sheets', [])])
    except HttpError as e:
        print('HttpError status:', e.resp.status)
        try:
            # More detailed content
            import json
            content = e.content.decode() if isinstance(e.content, (bytes, bytearray)) else str(e.content)
            print('Error content:', json.loads(content))
        except Exception:
            print('Raw error content:', e.content)
        raise

if __name__ == '__main__':
    run()
