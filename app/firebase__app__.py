from flask import Flask, request, jsonify, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# 🔐 Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Download from Google Cloud Console

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
client = gspread.authorize(credentials)

# Replace with your actual Google Sheet name

spreadsheet = client.open_by_key("1Oh6ezcoGomewnZia-qXjfrDbT5hGkW7lUn9dHWAMcj8")  # Example key
# sheet = client.open("Wedding Guest List").sheet1
sheet = spreadsheet.sheet1

# ✅ Helper function to find invite by number
def find_invite(invite_number):
    all_records = sheet.get_all_records()
    for row in all_records:
        if str(row["Invite Number"]).strip() == str(invite_number).strip():
            return row
    return None

@app.route('/')
def home():
    return render_template('index.html')  # You can use a template or React build here

# ✅ RSVP submission endpoint
@app.route('/rsvp', methods=['POST'])
def rsvp():
    data = request.json
    invite_number = data.get("invite_number")
    guest_names = data.get("guest_names", [])
    attending = data.get("attending", True)

    invite = find_invite(invite_number)
    if not invite:
        return jsonify({"error": "Invite number not found"}), 404

    allocated = int(invite.get("Seats Allocated", 0))
    if len(guest_names) > allocated:
        return jsonify({"error": f"Too many guests — max allowed is {allocated}"}), 400

    # ✅ Update Google Sheet
    row_index = sheet.find(invite_number).row
    sheet.update_cell(row_index, 4, ", ".join(guest_names))  # Update "Guest Names" column
    sheet.update_cell(row_index, 5, "Yes" if attending else "No")  # Update "RSVP" column

    return jsonify({"message": "RSVP recorded successfully"}), 200

# ✅ Admin route (password protected)
@app.route('/admin', methods=['GET'])
def admin():
    password = request.args.get("password")
    if password != "your_admin_password":
        return jsonify({"error": "Unauthorized"}), 403

    all_guests = sheet.get_all_records()
    return jsonify(all_guests)

if __name__ == "__main__":
    app.run(debug=True)
