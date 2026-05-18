package client;

import server.AirlineService;

import java.rmi.Naming;

public class RMIClient {

    public static AirlineService connect() {

        try {

            return (AirlineService)
                    Naming.lookup(
                            "rmi://localhost/AirlineService"
                    );

        } catch (Exception e) {

            e.printStackTrace();
            return null;
        }
    }
}