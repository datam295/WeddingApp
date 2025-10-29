import os
import json

def check_service_account():
    print("Checking service account setup...")
    
    # Check if file exists
    if not os.path.exists('service-account.json'):
        print("❌ service-account.json not found")
        return
    
    # Try to read and parse the file
    try:
        with open('service-account.json', 'r') as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = [
            'type',
            'project_id',
            'private_key_id',
            'private_key',
            'client_email',
            'client_id'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            print("❌ Service account file is missing required fields:", missing_fields)
        else:
            print("✓ Service account file contains all required fields")
            print(f"Project ID: {data['project_id']}")
            print(f"Client Email: {data['client_email']}")
    
    except json.JSONDecodeError:
        print("❌ Service account file is not valid JSON")
    except Exception as e:
        print(f"❌ Error reading service account file: {str(e)}")

if __name__ == "__main__":
    check_service_account()