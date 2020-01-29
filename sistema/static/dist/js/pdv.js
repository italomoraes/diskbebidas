app = angular.module("controllerApp", []);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

app.controller('controlesCtrl', function($scope, $http){
	$scope.venda_pk = parseInt(location.href.split('/')[location.href.split('/').length-2])
	$scope.qtd_modal = "1";
	$scope.buscarInput = "";
	$scope.itensNoCarrinho = [];
	$scope.valorTotalDoCarrinho = 0.00;

	$scope.adicionar = function(qtd) {
		data = {
			"qtd": qtd,
			"produto_pk": $scope.produto_pk,
			"venda_pk": $scope.venda_pk
		};
		$http.post('/api/addprodutotocart/', data).then(response => {
			// Rotina para adicionar o produto à lista
			data = JSON.parse(response.data);
			$scope.itensNoCarrinho = [];
			angular.forEach(data, (produto) => {
				$scope.itensNoCarrinho.push(produto.fields);
			});
		}, err => {
			// apresnetar mensagem de erro?
		});
		$scope.produto_pk = undefined;
	};

	$scope.buscar = function(input) {
		if(!(input=="")){
			$http.get('/api/consultaproduto/?codigo='+input).then(response => {
				data = JSON.parse(response.data)[0];
				$scope.produto_descricao = data.fields.descricao;
				$scope.produto_pk = data.pk;
				$('#addModal').modal();
			}, err => {
				console.log(err);
			});
		};
	};

	$scope.buscaProdutosVendidos = function() {
		$http.get('/api/getprodutosvendaatual/').then(response => {
			data = JSON.parse(response.data);
			angular.forEach(data, (produto) => {
				$scope.itensNoCarrinho.push(produto.fields)
			});
		}, err => {
			// apresentar alerta de erro?
		});
	}


});