(function () {
    angular.module("myApp")
        .controller("salidaCtrl", salidaCtrl);

    function salidaCtrl(SalidaService, $q) {
        var self = this;
        self.pedidos_selected = [];
        init();

        function init() {
            var promises = [loadPedidos(), loadUsers()];
            return $q.all(promises).then(function () {
            });
        }

        self.selectPedido = function (pedido) {
            self.pedidos_selected.push(pedido);
        };

        self.salidaCrear = function () {
            SalidaService.SalidaCrear.save({
                "pedidos": self.pedidos_selected,
                "user_selected": self.user_selected
            }, function (r) {


            }, function (err) {
                console.log(err);

            });
        };

        function loadPedidos() {

            SalidaService.PedidoList.query(function (r) {
                self.pedidos = r;
            });
        }

        function loadUsers() {

            SalidaService.UserList.query(function (r) {
                self.users = r;
                console.log(r);
            });
        }
    }
}());
