package server;

import database.FlightSearchDAO;
import database.ReservationDAO;
import database.UserDAO;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class AirlineServiceImpl
        extends UnicastRemoteObject
        implements AirlineService {

    UserDAO userDAO =
            new UserDAO();

    FlightSearchDAO flightDAO =
            new FlightSearchDAO();

    ReservationDAO reservationDAO =
            new ReservationDAO();

    public AirlineServiceImpl()
            throws RemoteException {

        super();
    }

    @Override
    public boolean registerUser(
            String name,
            String email,
            String phone,
            String password
    ) throws RemoteException {

        return userDAO.registerUser(
                name,
                email,
                phone,
                password
        );
    }

    @Override
    public boolean loginUser(
            String email,
            String password
    ) throws RemoteException {

        return userDAO.loginUser(
                email,
                password
        );
    }

    @Override
    public void searchFlights(
            String source,
            String destination
    ) throws RemoteException {

        flightDAO.searchFlights(
                source,
                destination
        );
    }

    @Override
    public boolean bookTicket(
            int userId,
            int scheduleId,
            String travelClass,
            int seatsRequired
    ) throws RemoteException {

        return reservationDAO.bookTicket(
                userId,
                scheduleId,
                travelClass,
                seatsRequired
        );
    }

    @Override
    public void viewReservations(
            int userId
    ) throws RemoteException {

        reservationDAO.viewReservations(
                userId
        );
    }

    @Override
    public boolean cancelReservation(
            int reservationId
    ) throws RemoteException {

        return reservationDAO.cancelReservation(
                reservationId
        );
    }
}