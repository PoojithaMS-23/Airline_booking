package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class FlightSearchDAO {

    public void searchFlights(
            String source,
            String destination
    ) {

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
                    "fs.available_first_class " +

                    "FROM flight_schedule fs " +

                    "JOIN flights f " +
                    "ON fs.flight_id = f.flight_id " +

                    "JOIN routes r " +
                    "ON fs.route_id = r.route_id " +

                    "WHERE r.source=? AND r.destination=?";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ps.setString(1, source);
            ps.setString(2, destination);

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
                        "Departure: "
                        + rs.getString("departure_time")
                );

                System.out.println(
                        "Economy Seats: "
                        + rs.getInt("available_economy")
                );

                System.out.println(
                        "Business Seats: "
                        + rs.getInt("available_business")
                );

                System.out.println(
                        "First Class Seats: "
                        + rs.getInt("available_first_class")
                );

                System.out.println(
                        "==========================="
                );
            }

            conn.close();

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}