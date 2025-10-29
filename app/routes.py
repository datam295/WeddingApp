from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
            thank_you_message = f"Thank you, {name}, for your RSVP! We look forward to seeing you at the wedding."
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
