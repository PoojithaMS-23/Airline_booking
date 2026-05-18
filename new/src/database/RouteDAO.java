package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class RouteDAO {

    public void viewRoutes() {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =
                    "SELECT * FROM routes";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ResultSet rs =
                    ps.executeQuery();

            while (rs.next()) {

                System.out.println(
                        "Route ID: "
                        + rs.getInt("route_id")
                );

                System.out.println(
                        "Source: "
                        + rs.getString("source")
                );

                System.out.println(
                        "Destination: "
                        + rs.getString("destination")
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