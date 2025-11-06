import os
import qrcode
from app.sheets_service import GuestList

# Set this to your deployed RSVP URL root
RSVP_URL_ROOT = "https://kabirandhennaswedding.co.uk/invite-number/"

# Output directory for QR codes
QR_DIR = "app/static/qrcodes"
os.makedirs(QR_DIR, exist_ok=True)

def main():
    guest_list = GuestList()
    # Fetch all invite numbers from the sheet
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    if not rows or len(rows) < 2:
        print("No guest data found.")
        return
    header = rows[0]
    data = rows[1:]
    for row in data:
        if len(row) > 0:
            invite_number = str(row[0]).strip()
            if invite_number:
                url = f"{RSVP_URL_ROOT}{invite_number}"
                img = qrcode.make(url)
                img_path = os.path.join(QR_DIR, f"invite_{invite_number}.png")
                img.save(img_path)
                print(f"Generated QR for invite {invite_number}: {img_path}")

if __name__ == "__main__":
    main()
