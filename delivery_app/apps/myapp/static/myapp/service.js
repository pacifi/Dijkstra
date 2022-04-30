(function () {
    "use strict";
    angular.module("myApp")
        .factory("SalidaService", ["$resource", SalidaService]);

    function SalidaService($resource) {
        var url = "/app";
        var params = {'id': '@id'};
        var methods = {"update": {method: 'PUT'}};
        return {
            PedidoList: $resource(url + "/pedido/service_list/:id/", params, methods),
            UserList: $resource(url + "/user/service_list/:id/", params, methods),
            SalidaCrear: $resource(url + "/salida/service_add/:id/", params, methods),
        };
    }
}());