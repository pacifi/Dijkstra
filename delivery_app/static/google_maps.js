
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + 'AIzaSyCl1VjvDOY5DNo_4xihLrfMTJAucvyQHBw' + "&libraries=places")
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initMap)

});


function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: {lat: lat_a, lng: long_a}
    });


    directionsDisplay.setMap(map);

    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {

    directionsService.route({
        origin: "-15.490264006767994,-70.12503423607635",
        destination: destination,
      //  destination: "-15.474641006051206,-70.15973665631103",
        travelMode: 'DRIVING'
    }, function(response, status) {

      if (status === 'OK') {
        directionsDisplay.setDirections(response);


      } else {

        alert('Directions request failed due to ' + status);
        // window.location.assign("/route")
      }
    });
}