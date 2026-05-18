package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class ReservationDAO {

    // BOOK TICKET
    public synchronized boolean bookTicket(

            int userId,
            int scheduleId,
            String travelClass,
            int seatsRequired
    ) {

        try {

            Connection conn =
                    DBConnection.getConnection();

            conn.setAutoCommit(false);

            String seatColumn = "";
            String priceColumn = "";

            if (
                    travelClass.equalsIgnoreCase(
                            "Economy"
                    )
            ) {

                seatColumn =
                        "available_economy";

                priceColumn =
                        "economy_price";

            } else if (
                    travelClass.equalsIgnoreCase(
                            "Business"
                    )
            ) {

                seatColumn =
                        "available_business";

                priceColumn =
                        "business_price";

            } else {

                seatColumn =
                        "available_first_class";

                priceColumn =
                        "first_class_price";
            }

            // CHECK AVAILABLE SEATS
            String checkQuery =

                    "SELECT " +

                    seatColumn +

                    ", " +

                    priceColumn +

                    " FROM flight_schedule " +

                    "WHERE schedule_id=?";

            PreparedStatement checkPs =
                    conn.prepareStatement(
                            checkQuery
                    );

            checkPs.setInt(
                    1,
                    scheduleId
            );

            ResultSet rs =
                    checkPs.executeQuery();

            if (!rs.next()) {

                conn.rollback();

                return false;
            }

            int availableSeats =
                    rs.getInt(seatColumn);

            double price =
                    rs.getDouble(priceColumn);

            if (
                    availableSeats
                            < seatsRequired
            ) {

                System.out.println(
                        "Not enough seats available"
                );

                conn.rollback();

                return false;
            }

            // UPDATE SEATS
            String updateQuery =

                    "UPDATE flight_schedule SET " +

                    seatColumn +

                    " = " +

                    seatColumn +

                    " - ? WHERE schedule_id=?";

            PreparedStatement updatePs =
                    conn.prepareStatement(
                            updateQuery
                    );

            updatePs.setInt(
                    1,
                    seatsRequired
            );

            updatePs.setInt(
                    2,
                    scheduleId
            );

            updatePs.executeUpdate();

            double totalAmount =
                    price * seatsRequired;

            // INSERT RESERVATION
            String reservationQuery =

                    "INSERT INTO reservations(" +

                    "user_id," +
                    "schedule_id," +
                    "travel_class," +
                    "seats_booked," +
                    "total_amount," +
                    "status" +

                    ") VALUES(?,?,?,?,?,?)";

            PreparedStatement reservationPs =
                    conn.prepareStatement(
                            reservationQuery
                    );

            reservationPs.setInt(
                    1,
                    userId
            );

            reservationPs.setInt(
                    2,
                    scheduleId
            );

            reservationPs.setString(
                    3,
                    travelClass
            );

            reservationPs.setInt(
                    4,
                    seatsRequired
            );

            reservationPs.setDouble(
                    5,
                    totalAmount
            );

            reservationPs.setString(
                    6,
                    "CONFIRMED"
            );

            reservationPs.executeUpdate();

            conn.commit();

            conn.close();

            System.out.println(
                    "Ticket Booked Successfully"
            );

            return true;

        } catch (Exception e) {

            e.printStackTrace();

            return false;
        }
    }

    // VIEW RESERVATIONS
    public void viewReservations(
            int userId
    ) {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =
                    "SELECT * FROM reservations WHERE user_id=?";

            PreparedStatement ps =
                    conn.prepareStatement(
                            query
                    );

            ps.setInt(1, userId);

            ResultSet rs =
                    ps.executeQuery();

            while (rs.next()) {

                System.out.println(
                        "Reservation ID: "
                        + rs.getInt(
                                "reservation_id"
                        )
                );

                System.out.println(
                        "Schedule ID: "
                        + rs.getInt(
                                "schedule_id"
                        )
                );

                System.out.println(
                        "Travel Class: "
                        + rs.getString(
                                "travel_class"
                        )
                );

                System.out.println(
                        "Seats Booked: "
                        + rs.getInt(
                                "seats_booked"
                        )
                );

                System.out.println(
                        "Total Amount: "
                        + rs.getDouble(
                                "total_amount"
                        )
                );

                System.out.println(
                        "Status: "
                        + rs.getString(
                                "status"
                        )
                );

                System.out.println(
                        "======================="
                );
            }

            conn.close();

        } catch (Exception e) {

            e.printStackTrace();
        }
    }

    // CANCEL RESERVATION
    public synchronized boolean cancelReservation(
            int reservationId
    ) {

        try {

            Connection conn =
                    DBConnection.getConnection();

            conn.setAutoCommit(false);

            String getQuery =
                    "SELECT * FROM reservations WHERE reservation_id=?";

            PreparedStatement getPs =
                    conn.prepareStatement(
                            getQuery
                    );

            getPs.setInt(
                    1,
                    reservationId
            );

            ResultSet rs =
                    getPs.executeQuery();

            if (!rs.next()) {

                conn.rollback();

                return false;
            }

            int scheduleId =
                    rs.getInt(
                            "schedule_id"
                    );

            String travelClass =
                    rs.getString(
                            "travel_class"
                    );

            int seatsBooked =
                    rs.getInt(
                            "seats_booked"
                    );

            String seatColumn = "";

            if (
                    travelClass.equalsIgnoreCase(
                            "Economy"
                    )
            ) {

                seatColumn =
                        "available_economy";

            } else if (
                    travelClass.equalsIgnoreCase(
                            "Business"
                    )
            ) {

                seatColumn =
                        "available_business";

            } else {

                seatColumn =
                        "available_first_class";
            }

            // RESTORE SEATS
            String updateQuery =

                    "UPDATE flight_schedule SET " +

                    seatColumn +

                    " = " +

                    seatColumn +

                    " + ? WHERE schedule_id=?";

            PreparedStatement updatePs =
                    conn.prepareStatement(
                            updateQuery
                    );

            updatePs.setInt(
                    1,
                    seatsBooked
            );

            updatePs.setInt(
                    2,
                    scheduleId
            );

            updatePs.executeUpdate();

            // DELETE RESERVATION
            String deleteQuery =
                    "DELETE FROM reservations WHERE reservation_id=?";

            PreparedStatement deletePs =
                    conn.prepareStatement(
                            deleteQuery
                    );

            deletePs.setInt(
                    1,
                    reservationId
            );

            deletePs.executeUpdate();

            conn.commit();

            conn.close();

            System.out.println(
                    "Reservation Cancelled"
            );

            return true;

        } catch (Exception e) {

            e.printStackTrace();

            return false;
        }
    }
}