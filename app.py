from flask import Flask, render_template, request, redirect
import urllib.parse

app = Flask(__name__)

# Room Data
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

@app.route("/")
def home():
    return render_template("index.html", rooms=rooms)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    phone = request.form.get("phone")
    room = request.form.get("room")
    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")

    message = f"""
Hello CPAK LOUNGE,

I would like to book a room.

Name: {name}
Phone: {phone}
Room: {room}
Check-in Date: {checkin}
Check-out Date: {checkout}

Please confirm availability. Thank you.
"""

    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/2349112113542?text={encoded_message}"

    return redirect(whatsapp_url)

if __name__ == "__main__":
    app.run(debug=True)