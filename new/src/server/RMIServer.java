package server;

import java.rmi.Naming;
import java.rmi.registry.LocateRegistry;

public class RMIServer {

    public static void main(String[] args) {

        try {

            LocateRegistry.createRegistry(1099);

            AirlineService service =
                    new AirlineServiceImpl();

            Naming.rebind(
                    "rmi://localhost/AirlineService",
                    service
            );

            System.out.println(
                    "RMI Server Running"
            );

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}