package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class FlightDAO {

    public void viewFlights() {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =
                    "SELECT * FROM flights";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ResultSet rs =
                    ps.executeQuery();

            while (rs.next()) {

                System.out.println(
                        "Flight ID: "
                        + rs.getInt("flight_id")
                );

                System.out.println(
                        "Flight Name: "
                        + rs.getString("flight_name")
                );

                System.out.println(
                        "Economy Seats: "
                        + rs.getInt("economy_seats")
                );

                System.out.println(
                        "Business Seats: "
                        + rs.getInt("business_seats")
                );

                System.out.println(
                        "First Class Seats: "
                        + rs.getInt("first_class_seats")
                );

                System.out.println(
                        "----------------------"
                );
            }

            conn.close();

        } catch (Exception e) {

            e.printStackTrace();
        }
    }
}