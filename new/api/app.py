from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import xmlrpc.client

app = Flask(__name__)

CORS(app)

# MYSQL CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="airline_db"
)

cursor = db.cursor(dictionary=True)

# LOGIN
@app.route('/login', methods=['POST'])
def login():

    data = request.json

    query = """
    SELECT * FROM users
    WHERE email=%s AND password=%s
    """

    cursor.execute(
        query,
        (
            data['email'],
            data['password']
        )
    )

    user = cursor.fetchone()

    if user:

        return jsonify({
            "success": True,
            "userId": user['user_id']
        })

    return jsonify({
        "success": False
    })


# REGISTER
@app.route('/register', methods=['POST'])
def register():

    data = request.json

    query = """
    INSERT INTO users(name,email,phone,password)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            data['name'],
            data['email'],
            data['phone'],
            data['password']
        )
    )

    db.commit()

    return jsonify({
        "message": "Registered Successfully"
    })


# SEARCH FLIGHTS
# SEARCH FLIGHTS
@app.route('/search', methods=['GET'])
def search_flights():

    source = request.args.get('source')

    destination = request.args.get('destination')

    # CREATE FRESH CONNECTION
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="airline_db"
    )

    cursor = db.cursor(dictionary=True)

    query = """

    SELECT
    fs.schedule_id,
    f.flight_name,
    r.source,
    r.destination,
    fs.departure_time,

    fs.available_economy,
    fs.available_business,
    fs.available_first_class

    FROM flight_schedule fs

    JOIN flights f
    ON fs.flight_id = f.flight_id

    JOIN routes r
    ON fs.route_id = r.route_id

    WHERE r.source=%s
    AND r.destination=%s
    """

    cursor.execute(
        query,
        (
            source,
            destination
        )
    )

    flights = cursor.fetchall()

    # CLOSE CONNECTION
    cursor.close()
    db.close()

    return jsonify(flights)
# BOOK TICKET
# BOOK TICKET
@app.route('/book', methods=['POST'])
def book_ticket():

    data = request.json

    try:

        # CONNECT TO RPC SERVER
        proxy = xmlrpc.client.ServerProxy(
            "http://localhost:8000/"
        )

        # REMOTE PROCEDURE CALL
        result = proxy.book_ticket(

            int(data['userId']),

            int(data['scheduleId']),

            data['travelClass'],

            int(data['seatsRequired'])
        )

        if result:

            return jsonify({
                "message": "Ticket Booked Successfully"
            })

        return jsonify({
            "message": "Booking Failed - Seats Unavailable"
        }), 400

    except Exception as e:

        print(e)

        return jsonify({
            "message": "RPC Server Error"
        }), 500

# GET RESERVATIONS
@app.route('/reservations/<int:user_id>')
def reservations(user_id):

    query = """

    SELECT *

    FROM reservations

    WHERE user_id=%s
    """

    cursor.execute(
        query,
        (user_id,)
    )

    result = cursor.fetchall()

    return jsonify(result)


# CANCEL RESERVATION
@app.route('/cancel/<int:reservation_id>',
methods=['DELETE'])

def cancel_reservation(reservation_id):

    # GET RESERVATION
    query = """

    SELECT *

    FROM reservations

    WHERE reservation_id=%s
    """

    cursor.execute(
        query,
        (reservation_id,)
    )

    reservation = cursor.fetchone()

    if not reservation:

        return jsonify({
            "message": "Reservation not found"
        })

    travel_class = reservation['travel_class']

    seats_booked = reservation['seats_booked']

    schedule_id = reservation['schedule_id']

    if travel_class == "Economy":

        seat_column = "available_economy"

    elif travel_class == "Business":

        seat_column = "available_business"

    else:

        seat_column = "available_first_class"

    # RESTORE SEATS
    restore_query = f"""

    UPDATE flight_schedule

    SET {seat_column} =
    {seat_column} + %s

    WHERE schedule_id=%s
    """

    cursor.execute(
        restore_query,
        (
            seats_booked,
            schedule_id
        )
    )

    # DELETE RESERVATION
    delete_query = """

    DELETE FROM reservations

    WHERE reservation_id=%s
    """

    cursor.execute(
        delete_query,
        (reservation_id,)
    )

    db.commit()

    return jsonify({
        "message": "Reservation Cancelled"
    })


if __name__ == '__main__':

    app.run(debug=True)