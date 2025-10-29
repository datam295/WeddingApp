from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os.path
import json

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
    try:
        creds = None
        # Look for service account credentials first
        if os.path.exists('app/service-account.json'):
            creds = Credentials.from_service_account_file(
                'service-account.json', 
                scopes=SCOPES
            )
        else:
            print("Error: service-account.json not found")
            return None
            
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error setting up service: {str(e)}")
        return None

    try:
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building service: {e}")
        return None

class GuestList:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.service = get_google_sheets_service()
        self.range_name = 'Sheet1!A:F'  # Adjust based on your sheet structure

    def validate_invite(self, invite_number):
        """Check if invite number exists and get allowed guests"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name
            ).execute()
            
            rows = result.get('values', [])
            for row in rows:
                if row[0] == invite_number:  # Assuming invite number is in first column
                    return {
                        'valid': True,
                        'max_guests': int(row[1]),  # Assuming max guests is in second column
                        'name': row[2],  # Assuming name is in third column
                        'row_index': rows.index(row) + 1
                    }
            return {'valid': False}
        except Exception as e:
            print(f"Error validating invite: {e}")
            return {'valid': False}

    def update_rsvp(self, row_index, attending, guests, attendees):
        """Update RSVP status in spreadsheet"""
        try:
            range_name = f'Sheet1!D{row_index}:F{row_index}'  # Columns for RSVP status, guest count, and attendee names
            values = [[
                'Yes' if attending == 'yes' else 'No',
                guests,
                attendees
            ]]
            body = {
                'values': values
            }
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            return True
        except Exception as e:
            print(f"Error updating RSVP: {e}")
            return False