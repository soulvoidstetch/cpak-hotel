from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================
# ROOM LIST
# ==============================

rooms = [

    # ₦18,000 Rooms
    {"name": "Montana", "price": 18000, "image": "montana.jpeg"},
    {"name": "Alaska", "price": 18000, "image": "alaska.jpeg"},
    {"name": "Hawali", "price": 18000, "image": "hawali.jpeg"},
    {"name": "Texas", "price": 18000, "image": "texas.jpeg"},
    {"name": "Georgia", "price": 18000, "image": "georgia.jpeg"},
    {"name": "Indianapolis", "price": 18000, "image": "indianapolis.jpeg"},
    {"name": "Maryland", "price": 18000, "image": "maryland.jpeg"},
    {"name": "New Jersey", "price": 18000, "image": "newjersey.jpeg"},

    # ₦20,000 Rooms
    {"name": "New York", "price": 20000, "image": "newyork.jpeg"},
    {"name": "New Mexico", "price": 20000, "image": "newmexico.jpeg"},
    {"name": "Atlanta", "price": 20000, "image": "atlanta.jpeg"},
    {"name": "Michigan", "price": 20000, "image": "michigan.jpeg"},
    {"name": "Washington", "price": 20000, "image": "washington.jpeg"},
    {"name": "Oregon", "price": 20000, "image": "oregon.jpeg"},
    {"name": "California", "price": 20000, "image": "california.jpeg"},
    {"name": "Florida", "price": 20000, "image": "florida.jpeg"},
]

# ==============================
# DATABASE MODEL
# ==============================

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    room = db.Column(db.String(100))
    checkin = db.Column(db.String(20))
    checkout = db.Column(db.String(20))


# ==============================
# HOME ROUTE
# ==============================

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        booking = Booking(
            name=request.form["name"],
            phone=request.form["phone"],
            room=request.form["room"],
            checkin=request.form["checkin"],
            checkout=request.form["checkout"],
        )

        db.session.add(booking)
        db.session.commit()

        message = f"""
Hello CPAK Lounge,

I just booked:

Room: {booking.room}
Name: {booking.name}
Phone: {booking.phone}
Check-in: {booking.checkin}
Check-out: {booking.checkout}

Please confirm availability.
"""

        encoded_message = urllib.parse.quote(message)

        # 🔥 REPLACE WITH YOUR REAL NUMBER
        whatsapp_number = "2348012345678"

        return redirect(f"https://wa.me/{whatsapp_number}?text={encoded_message}")

    return render_template("index.html", rooms=rooms)


# ==============================
# ADMIN PAGE
# ==============================

@app.route("/admin")
def admin():
    bookings = Booking.query.all()
    return render_template("admin.html", bookings=bookings)


# ==============================
# RUN APP
# ==============================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)