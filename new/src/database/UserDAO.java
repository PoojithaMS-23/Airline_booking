package database;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class UserDAO {

    public boolean registerUser(
            String name,
            String email,
            String phone,
            String password
    ) {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =
                    "INSERT INTO users(name,email,phone,password) VALUES(?,?,?,?)";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ps.setString(1, name);
            ps.setString(2, email);
            ps.setString(3, phone);
            ps.setString(4, password);

            int rows =
                    ps.executeUpdate();

            conn.close();

            return rows > 0;

        } catch (Exception e) {

            e.printStackTrace();

            return false;
        }
    }

    public boolean loginUser(
            String email,
            String password
    ) {

        try {

            Connection conn =
                    DBConnection.getConnection();

            String query =
                    "SELECT * FROM users WHERE email=? AND password=?";

            PreparedStatement ps =
                    conn.prepareStatement(query);

            ps.setString(1, email);
            ps.setString(2, password);

            ResultSet rs =
                    ps.executeQuery();

            boolean found = rs.next();

            conn.close();

            return found;

        } catch (Exception e) {

            e.printStackTrace();

            return false;
        }
    }
}