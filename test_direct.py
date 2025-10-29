from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os

def test_direct_connection():
    print("Testing direct Google Sheets connection")
    print("-" * 30)
    
    try:
        # Get credentials
        creds = Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        print("✓ Loaded credentials")
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        print("✓ Built service")
        
        # Try to access the spreadsheet
        SPREADSHEET_ID = os.getenv('WEDDING_SHEET_ID', 'your-spreadsheet-id-here')
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='A1:A1'
        ).execute()
        
        print("✓ Successfully accessed spreadsheet")
        print(f"Data retrieved: {result.get('values', [])}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    test_direct_connection()