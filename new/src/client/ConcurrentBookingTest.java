package client;

import server.AirlineService;

public class ConcurrentBookingTest {

    public static void main(String[] args) {

        Runnable bookingTask = () -> {

            try {

                AirlineService service =
                        RMIClient.connect();

                String clientName =
                        Thread.currentThread().getName();

                System.out.println(
                        clientName
                        + " attempting booking..."
                );

                boolean result =
                        service.bookTicket(
                                1,              // userId
                                1,              // scheduleId
                                "Business",     // class
                                2               // seats
                        );

                if (result) {

                    System.out.println(
                            clientName
                            + " Booking Successful"
                    );

                } else {

                    System.out.println(
                            clientName
                            + " Booking Failed"
                    );
                }

            } catch (Exception e) {

                e.printStackTrace();
            }
        };

        Thread client1 =
                new Thread(
                        bookingTask,
                        "Client-1"
                );

        Thread client2 =
                new Thread(
                        bookingTask,
                        "Client-2"
                );

        Thread client3 =
                new Thread(
                        bookingTask,
                        "Client-3"
                );

        client1.start();

        client2.start();

        client3.start();
    }
}