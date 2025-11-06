from flask import Flask, render_template
from app.sheets_service import GuestList

app = Flask(__name__)

@app.route('/print-cards')
def print_cards():
    guest_list = GuestList()
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    if not rows or len(rows) < 2:
        return "No guest data found."
    data = rows[1:]
    invites = []
    for row in data:
        if len(row) > 0:
            invite_number = str(row[0]).strip()
            if invite_number:
                invites.append({'invite_number': invite_number})
    return render_template('rsvp_cards.html', invites=invites)

if __name__ == "__main__":
    app.run(debug=True)
