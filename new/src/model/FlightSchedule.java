package model;

public class FlightSchedule {

    private int scheduleId;

    private int flightId;

    private int routeId;

    private String departureTime;

    private int availableEconomy;

    private int availableBusiness;

    private int availableFirstClass;

    private double economyPrice;

    private double businessPrice;

    private double firstClassPrice;

    public FlightSchedule() {
    }

    public int getScheduleId() {
        return scheduleId;
    }

    public void setScheduleId(int scheduleId) {
        this.scheduleId = scheduleId;
    }

    public int getFlightId() {
        return flightId;
    }

    public void setFlightId(int flightId) {
        this.flightId = flightId;
    }

    public int getRouteId() {
        return routeId;
    }

    public void setRouteId(int routeId) {
        this.routeId = routeId;
    }

    public String getDepartureTime() {
        return departureTime;
    }

    public void setDepartureTime(String departureTime) {
        this.departureTime = departureTime;
    }

    public int getAvailableEconomy() {
        return availableEconomy;
    }

    public void setAvailableEconomy(int availableEconomy) {
        this.availableEconomy = availableEconomy;
    }

    public int getAvailableBusiness() {
        return availableBusiness;
    }

    public void setAvailableBusiness(int availableBusiness) {
        this.availableBusiness = availableBusiness;
    }

    public int getAvailableFirstClass() {
        return availableFirstClass;
    }

    public void setAvailableFirstClass(int availableFirstClass) {
        this.availableFirstClass = availableFirstClass;
    }

    public double getEconomyPrice() {
        return economyPrice;
    }

    public void setEconomyPrice(double economyPrice) {
        this.economyPrice = economyPrice;
    }

    public double getBusinessPrice() {
        return businessPrice;
    }

    public void setBusinessPrice(double businessPrice) {
        this.businessPrice = businessPrice;
    }

    public double getFirstClassPrice() {
        return firstClassPrice;
    }

    public void setFirstClassPrice(double firstClassPrice) {
        this.firstClassPrice = firstClassPrice;
    }
}