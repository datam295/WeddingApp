from app.sheets_service import GuestList
import os

def test_sheets_connection():
    # Get the spreadsheet ID from environment variable
    SPREADSHEET_ID = os.getenv('WEDDING_SHEET_ID', 'your-spreadsheet-id-here')
    
    print("Testing Google Sheets Integration")
    print("-" * 30)
    
    try:
        # Initialize GuestList
        print("1. Initializing GuestList...")
        guest_list = GuestList(SPREADSHEET_ID)
        
        if guest_list.service is None:
            print("❌ Failed to initialize Google Sheets service")
            return False
        
        print("✓ Successfully initialized Google Sheets service")
        
        # Test invite validation
        print("\n2. Testing invite validation...")
        test_invite = "TEST123"  # Use a known test invite number
        result = guest_list.validate_invite(test_invite)
        
        print(f"Validation result for {test_invite}: {result}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_sheets_connection()
    print("\nTest completed. Success:", "✓" if success else "❌")