package server;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AirlineService extends Remote {

    boolean registerUser(
            String name,
            String email,
            String phone,
            String password
    ) throws RemoteException;

    boolean loginUser(
            String email,
            String password
    ) throws RemoteException;

    void searchFlights(
            String source,
            String destination
    ) throws RemoteException;

    boolean bookTicket(
            int userId,
            int scheduleId,
            String travelClass,
            int seatsRequired
    ) throws RemoteException;

    void viewReservations(
            int userId
    ) throws RemoteException;

    boolean cancelReservation(
            int reservationId
    ) throws RemoteException;
}