from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.parse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------
# DATABASE MODEL
# ----------------------

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    room = db.Column(db.String(100))
    checkin = db.Column(db.Date)
    checkout = db.Column(db.Date)

# ----------------------
# ROOM DATA
# ----------------------

rooms = [
    {"name": "Montana", "price": 18000, "image": "montana.jpeg"},
    {"name": "Alaska", "price": 18000, "image": "alaska.jpeg"},
    {"name": "Hawali", "price": 18000, "image": "hawali.jpeg"},
    {"name": "Texas", "price": 18000, "image": "texas.jpeg"},
    {"name": "Georgia", "price": 18000, "image": "georgia.jpeg"},
    {"name": "Indianapolis", "price": 18000, "image": "indianapolis.jpeg"},
    {"name": "Maryland", "price": 18000, "image": "maryland.jpeg"},
    {"name": "New Jersey", "price": 18000, "image": "newjersey.jpeg"},
    {"name": "New York", "price": 20000, "image": "newyork.jpeg"},
    {"name": "New Mexico", "price": 20000, "image": "newmexico.jpeg"},
    {"name": "Atlanta", "price": 20000, "image": "atlanta.jpeg"},
    {"name": "Michigan", "price": 20000, "image": "michigan.jpeg"},
    {"name": "Washington", "price": 20000, "image": "washington.jpeg"},
    {"name": "Oregon", "price": 20000, "image": "oregon.jpeg"},
    {"name": "California", "price": 20000, "image": "california.jpeg"},
    {"name": "Florida", "price": 20000, "image": "florida.jpeg"},
]

# ----------------------
# HOME PAGE
# ----------------------

@app.route("/")
def home():
    return render_template("index.html", rooms=rooms)

# ----------------------
# BOOKING ROUTE
# ----------------------

@app.route("/book", methods=["POST"])
def book():

    name = request.form.get("name")
    phone = request.form.get("phone")
    room = request.form.get("room")
    checkin = datetime.strptime(request.form.get("checkin"), "%Y-%m-%d")
    checkout = datetime.strptime(request.form.get("checkout"), "%Y-%m-%d")

    # CHECK AVAILABILITY
    existing_booking = Booking.query.filter(
        Booking.room == room,
        Booking.checkin <= checkout,
        Booking.checkout >= checkin
    ).first()

    if existing_booking:
        return "Room not available for selected dates. Please go back and choose different dates."

    # SAVE BOOKING
    new_booking = Booking(
        name=name,
        phone=phone,
        room=room,
        checkin=checkin,
        checkout=checkout
    )

    db.session.add(new_booking)
    db.session.commit()

    # WHATSAPP MESSAGE
    message = f"""
Hello CPAK LOUNGE,

New Booking:

Name: {name}
Phone: {phone}
Room: {room}
Check-in: {checkin.date()}
Check-out: {checkout.date()}
"""

    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/2349112113542?text={encoded_message}"

    return redirect(whatsapp_url)

# ----------------------
# ADMIN DASHBOARD
# ----------------------

@app.route("/admin")
def admin():
    bookings = Booking.query.all()
    return render_template("admin.html", bookings=bookings)

# ----------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)