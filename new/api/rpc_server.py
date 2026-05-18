from xmlrpc.server import SimpleXMLRPCServer

import mysql.connector

import threading

# GLOBAL LOCK
lock = threading.Lock()

# CREATE DATABASE CONNECTION
def get_db_connection():

    return mysql.connector.connect(

        host="localhost",
        user="root",
        password="root123",
        database="airline_db"
    )

# RPC FUNCTION
def book_ticket(

    user_id,
    schedule_id,
    travel_class,
    seats_required
):

    with lock:

        try:

            # NEW CONNECTION FOR EVERY REQUEST
            db = get_db_connection()

            cursor = db.cursor(
                dictionary=True
            )

            # DETERMINE SEAT COLUMN
            if travel_class == "Economy":

                seat_column ="available_economy"

            elif travel_class == "Business":

                seat_column ="available_business"

            else:

                seat_column ="available_first_class"

            # CHECK AVAILABLE SEATS
            query = f"""

            SELECT {seat_column}

            FROM flight_schedule

            WHERE schedule_id=%s
            """

            cursor.execute(

                query,

                (schedule_id,)
            )

            result = cursor.fetchone()

            if not result:

                return False

            available =result[seat_column]

            print(
                "Available Seats:",
                available
            )

            # NOT ENOUGH SEATS
            if available < seats_required:

                print(
                    "Not enough seats"
                )

                return False

            # UPDATE SEATS
            update_query = f"""

            UPDATE flight_schedule

            SET {seat_column} =
            {seat_column} - %s

            WHERE schedule_id=%s
            """

            cursor.execute(

                update_query,

                (
                    seats_required,
                    schedule_id
                )
            )

            # INSERT RESERVATION
            insert_query = """

            INSERT INTO reservations(

                user_id,
                schedule_id,
                travel_class,
                seats_booked,
                total_amount,
                status

            )

            VALUES(%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(

                insert_query,

                (
                    user_id,
                    schedule_id,
                    travel_class,
                    seats_required,
                    5000,
                    "CONFIRMED"
                )
            )

            # COMMIT CHANGES
            db.commit()

            print(
                "Booking Successful"
            )

            # CLOSE CONNECTION
            cursor.close()

            db.close()

            return True

        except Exception as e:

            print("RPC ERROR:", e)

            return False

# START RPC SERVER
server = SimpleXMLRPCServer(

    ("localhost", 8000),

    allow_none=True
)

print("RPC Server Running On Port 8000...")

# REGISTER FUNCTION
server.register_function(

    book_ticket,

    "book_ticket"
)

# START SERVER
server.serve_forever()