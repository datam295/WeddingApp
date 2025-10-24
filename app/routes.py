from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')


@main.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    if request.method == "POST":
        invite_number = request.form.get("invite_number")
        name = request.form.get("name")
        attendees = request.form.get("attendees")
        guests = request.form.get("guests")
        attending = request.form.get("attending")

        # Save or process RSVP
        # e.g., save_to_csv(invite_number, name, attendees, guests, attending)

        return render_template("rsvp.html", submitted=True, name=name)
    return render_template("rsvp.html", submitted=False)



@main.route('/wedding-info')
def wedding_info():
    return render_template('wedding_info.html')

@main.route('/reception-info')
def reception_info():
    return render_template('reception_info.html')
