package model;

public class Reservation {

    private int reservationId;
    private int userId;
    private int scheduleId;

    private String travelClass;

    private int seatsBooked;

    private double totalAmount;

    private String status;

    public Reservation() {
    }

    public Reservation(
            int reservationId,
            int userId,
            int scheduleId,
            String travelClass,
            int seatsBooked,
            double totalAmount,
            String status
    ) {

        this.reservationId = reservationId;
        this.userId = userId;
        this.scheduleId = scheduleId;
        this.travelClass = travelClass;
        this.seatsBooked = seatsBooked;
        this.totalAmount = totalAmount;
        this.status = status;
    }

    public int getReservationId() {
        return reservationId;
    }

    public void setReservationId(int reservationId) {
        this.reservationId = reservationId;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public int getScheduleId() {
        return scheduleId;
    }

    public void setScheduleId(int scheduleId) {
        this.scheduleId = scheduleId;
    }

    public String getTravelClass() {
        return travelClass;
    }

    public void setTravelClass(String travelClass) {
        this.travelClass = travelClass;
    }

    public int getSeatsBooked() {
        return seatsBooked;
    }

    public void setSeatsBooked(int seatsBooked) {
        this.seatsBooked = seatsBooked;
    }

    public double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(double totalAmount) {
        this.totalAmount = totalAmount;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}