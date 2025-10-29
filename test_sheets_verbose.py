from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sheets_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def test_direct_connection():
    logging.info("Starting Google Sheets connection test")
    
    try:
        # Check current directory
        logging.info(f"Current working directory: {os.getcwd()}")
        
        # Check if service account file exists
        service_account_path = 'service-account.json'
        if os.path.exists(service_account_path):
            logging.info(f"Service account file found at {service_account_path}")
        else:
            logging.error(f"Service account file not found at {service_account_path}")
            return False

        # Get credentials
        logging.info("Loading credentials...")
        creds = Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        logging.info("Credentials loaded successfully")
        
        # Build service
        logging.info("Building Google Sheets service...")
        service = build('sheets', 'v4', credentials=creds)
        logging.info("Service built successfully")
        
        # Try to access the spreadsheet
        SPREADSHEET_ID = os.getenv('WEDDING_SHEET_ID', 'your-spreadsheet-id-here')
        logging.info(f"Attempting to access spreadsheet: {SPREADSHEET_ID}")
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='A1:A1'
        ).execute()
        
        logging.info("Successfully accessed spreadsheet")
        logging.info(f"Data retrieved: {result.get('values', [])}")
        return True
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_direct_connection()
    logging.info(f"Test completed. Success: {success}")
    
    # Print final status to console
    with open('sheets_test.log', 'r') as f:
        print("\nTest Log:")
        print("-" * 50)
        print(f.read())