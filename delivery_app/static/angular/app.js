(function () {
    var app = angular.module("myApp", [
        'ngResource',
    ]);
    app.config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });



}());
