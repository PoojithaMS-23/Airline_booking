package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class FlightScheduleDAO {

    public void viewFlightSchedules() {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =

                    "SELECT " +
                    "fs.schedule_id, " +
                    "f.flight_name, " +
                    "r.source, " +
                    "r.destination, " +
                    "fs.departure_time, " +

                    "fs.available_economy, " +
                    "fs.available_business, " +
                    "fs.available_first_class, " +

                    "fs.economy_price, " +
                    "fs.business_price, " +
                    "fs.first_class_price " +

                    "FROM flight_schedule fs " +

                    "JOIN flights f " +
                    "ON fs.flight_id = f.flight_id " +

                    "JOIN routes r " +
                    "ON fs.route_id = r.route_id";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ResultSet rs =
                    ps.executeQuery();

            while (rs.next()) {

                System.out.println(
                        "Schedule ID: "
                        + rs.getInt("schedule_id")
                );

                System.out.println(
                        "Flight Name: "
                        + rs.getString("flight_name")
                );

                System.out.println(
                        "Route: "
                        + rs.getString("source")
                        + " -> "
                        + rs.getString("destination")
                );

                System.out.println(
                        "Departure Time: "
                        + rs.getString("departure_time")
                );

                System.out.println(
                        "Available Economy Seats: "
                        + rs.getInt("available_economy")
                );

                System.out.println(
                        "Available Business Seats: "
                        + rs.getInt("available_business")
                );

                System.out.println(
                        "Available First Class Seats: "
                        + rs.getInt("available_first_class")
                );

                System.out.println(
                        "===================================="
                );
            }

            conn.close();

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}