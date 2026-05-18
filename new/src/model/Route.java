package model;

public class Route {

    private int routeId;
    private String source;
    private String destination;

    public Route() {
    }

    public Route(
            int routeId,
            String source,
            String destination
    ) {
        this.routeId = routeId;
        this.source = source;
        this.destination = destination;
    }

    public int getRouteId() {
        return routeId;
    }

    public void setRouteId(int routeId) {
        this.routeId = routeId;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
    }
}