/*jshint strict:false */
/*global $, console, alert, google, autocomplete_a , autocomplete_b, autocomplete_c, autocomplete_d, google_api_key, url */
/*jshint esversion: 6 */


$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function (script, textStatus) {
        google.maps.event.addDomListener(window, "load", initMap);

    });


function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7, center: {lat: lat_a, lng: long_a}
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);
}

var puntos = [];

if (cantidad == 3) {
    puntos.push({
        location:
            {lat: lat_c, lng: long_c}, stopover: true
    });
}
if (cantidad == 4) {
    puntos.push({
        location:
            {lat: lat_c, lng: long_c}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_d, lng: long_d}, stopover: true
    });
}
if (cantidad == 5) {
    puntos.push({
        location:
            {lat: lat_c, lng: long_c}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_d, lng: long_d}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_e, lng: long_e}, stopover: true
    });
}
if (cantidad == 6) {
    puntos.push({
        location:
            {lat: lat_c, lng: long_c}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_d, lng: long_d}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_e, lng: long_e}, stopover: true
    });
    puntos.push({
        location:
            {lat: lat_f, lng: long_f}, stopover: true
    });

}

const waypts = puntos;


function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);


        } else {

            alert('Directions request failed due to ' + status);
            window.location.assign("/route");
        }
    });
}