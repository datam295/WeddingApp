import qrcode
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from .sheets_service import GuestList
import os

main = Blueprint('main', __name__)


# Initialize GuestList with your Google Sheet ID
SPREADSHEET_ID = os.getenv('WEDDING_SHEET_ID', 'your-spreadsheet-id-here')
guest_list = GuestList(SPREADSHEET_ID)

@main.route('/')
def home():
    return render_template('index.html')

@main.route("/validate-invite/<invite_number>")
def validate_invite(invite_number):
    result = guest_list.validate_invite(invite_number)
    return jsonify(result)

@main.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        invite_number = request.form.get("invite_number")
        name = request.form.get("name")
        attendees = request.form.get("attendees")
        guests = int(request.form.get("guests"))
        attending = request.form.get("attending")

        # Validate invite number and guest count
        validation = guest_list.validate_invite(invite_number)
        
        if not validation['valid']:
            flash("Invalid invite number. Please check and try again.", "error")
            return render_template("rsvp.html", submitted=False, error=True)

        if guests > validation['max_guests']:
            flash(f"We're sorry, but the maximum number of guests allowed for your invitation is {validation['max_guests']}. Please adjust your RSVP and resubmit. Thank you!", "error")
            return render_template("rsvp.html", submitted=False, error=True, max_guests=validation['max_guests'])

        # Update the spreadsheet
        if guest_list.update_rsvp(validation['row_index'], attending, guests, attendees):
            thank_you_message = f"Thank you, {name}, for your RSVP! We look forward to seeing you at the wedding Reception."
            return render_template("rsvp.html", submitted=True, name=name, thank_you_message=thank_you_message)
        else:
            flash("There was an error processing your RSVP. Please try again.", "error")
            return render_template("rsvp.html", submitted=False, error=True)
            
    return render_template("rsvp.html", submitted=False)



@main.route('/wedding-info')
def wedding_info():
    return render_template('wedding_info.html')

@main.route('/reception-info')
def reception_info():
    return render_template('reception_info.html')

@main.route('/admin')
def admin():
    # Fetch all guest data from the sheet
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    header = rows[0] if rows else []
    data = rows[1:] if len(rows) > 1 else []

    # Indices for relevant columns
    RSVP_STATUS_IDX = 3  # D column: RSVP Status
    GUEST_COUNT_IDX = 4  # E column: Actual Guest Count

    total_rsvps = 0
    pending_rsvps = 0
    total_guests_confirmed = 0
    for row in data:
        status = row[RSVP_STATUS_IDX] if len(row) > RSVP_STATUS_IDX else ''
        guest_count = int(row[GUEST_COUNT_IDX]) if len(row) > GUEST_COUNT_IDX and row[GUEST_COUNT_IDX].isdigit() else 0
        if status.strip().lower() == 'yes':
            total_rsvps += 1
            total_guests_confirmed += guest_count
        elif status.strip() == '' or status.strip().lower() == 'pending':
            pending_rsvps += 1

    return render_template('admin.html',
        total_rsvps=total_rsvps,
        pending_rsvps=pending_rsvps,
        total_guests_confirmed=total_guests_confirmed
    )

@main.route('/admin/pending')
def admin_pending():
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    header = rows[0] if rows else []
    data = rows[1:] if len(rows) > 1 else []
    RSVP_STATUS_IDX = 3
    pending = [row for row in data if len(row) > RSVP_STATUS_IDX and (row[RSVP_STATUS_IDX].strip() == '' or row[RSVP_STATUS_IDX].strip().lower() == 'pending')]
    return render_template('admin_list.html', header=header, rows=pending, title='Pending RSVPs')

@main.route('/admin/accepted')
def admin_accepted():
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    header = rows[0] if rows else []
    data = rows[1:] if len(rows) > 1 else []
    RSVP_STATUS_IDX = 3
    accepted = [row for row in data if len(row) > RSVP_STATUS_IDX and row[RSVP_STATUS_IDX].strip().lower() == 'yes']
    return render_template('admin_list.html', header=header, rows=accepted, title='Accepted RSVPs')

@main.route('/invite-number/<invite_number>', methods=["GET"])
def invite_number_rsvp(invite_number):
    validation = guest_list.validate_invite(invite_number)
    if not validation['valid']:
        flash("Invalid invite number. Please check and try again.", "error")
        return render_template("rsvp.html", submitted=False, error=True)
    # Pre-populate the RSVP form with invite data
    return render_template(
        "rsvp.html",
        submitted=False,
        invite_number=invite_number,
        name=validation.get('name', ''),
        max_guests=validation.get('max_guests', ''),
        attendees=validation.get('attendees', ''),
        attending=validation.get('attending', ''),
        error=False
    )

@main.route('/print-cards')
def print_cards():
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
            name = row[1].strip() if len(row) > 1 else ''
            if invite_number:
                invites.append({'invite_number': invite_number, 'name': name})
    return render_template('rsvp_cards.html', invites=invites)

# ...existing code...
# Route to generate QR codes for all invites
@main.route('/admin/generate-qrcodes')
def generate_qrcodes():
    RSVP_URL_ROOT = "https://kabirandhennaswedding.co.uk/invite-number/"
    QR_DIR = os.path.join(current_app.root_path, 'static', 'qrcodes')
    os.makedirs(QR_DIR, exist_ok=True)
    guest_list = GuestList()
    result = guest_list.service.spreadsheets().values().get(
        spreadsheetId=guest_list.spreadsheet_id,
        range=guest_list.range_name
    ).execute()
    rows = result.get('values', [])
    if not rows or len(rows) < 2:
        return "No guest data found."
    data = rows[1:]
    count = 0
    for row in data:
        if len(row) > 0:
            invite_number = str(row[0]).strip()
            if invite_number:
                url = f"{RSVP_URL_ROOT}{invite_number}"
                img = qrcode.make(url)
                img_path = os.path.join(QR_DIR, f"invite_{invite_number}.png")
                img.save(img_path)
                count += 1
    return f"Generated {count} QR codes in static/qrcodes."

