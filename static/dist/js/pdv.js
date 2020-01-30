app = angular.module("controllerApp", []);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

app.directive('ngEnter', function() {
    return function(scope, element, attrs) {
        element.bind("keydown keypress", function(event) {
            if(event.which === 13) {
                scope.$apply(function(){
                    scope.$eval(attrs.ngEnter, {'event': event});
                });
                event.preventDefault();
            }
        });
    };
});

app.controller('controlesCtrl', function($scope, $http){
	$scope.venda_pk = parseInt(location.href.split('/')[location.href.split('/').length-2])
	$scope.qtd_modal = "1";
	$scope.produto_valor_modal = "0.00";
	$scope.buscarInput = "";
	$scope.itensNoCarrinho = [];
	$scope.valorTotalDoCarrinho = 0.00;
	$scope.erroTexto = "";
	$scope.produtosBusca = [];
	$scope.sucessoTexto = "";
	$scope.formasDePagamento = [{"nome": "Dinheiro", "valor": "DI"}, {"nome": "Crédito", "valor": "CR"}, {"nome": "Débito", "valor": "DE"}];
	$scope.finalizaMensagensFlag = false;
	$scope.finalizaMensagem;
	$scope.descontoComboFlag = false;
	$scope.caixaLivre = true;

	$('#addModal').on('shown.bs.modal', function () {
		$('#qtd_modal').trigger('focus')
	});
	$('#sucessoModal').on('hide.bs.modal', function () {
		if($scope.sucessoTexto == "Venda cancelada com sucesso."){
			$scope.buscaProdutosVendidos()
		} else if ($scope.sucessoTexto == "Venda finalizada com sucesso.") {
			location.href="/pdv/";
		};
	});

	$scope.adicionar = function(qtd) {
		let data = {
			"qtd": qtd,
			"produto_pk": $scope.produto_pk,
			"venda_pk": $scope.venda_pk
		};
		$http.post('/api/addprodutotocart/', data).then(response => {
			// Rotina para adicionar o produto à lista
			let data = JSON.parse(response.data);
			$scope.itensNoCarrinho = [];
			$scope.valorTotalDoCarrinho = 0.00;
			$scope.descontoComboFlag = false;
			if (data.length == 0){
				$scope.caixaLivre = true;
			} else {
				$scope.caixaLivre = false;
				angular.forEach(data, (produto) => {
					$scope.itensNoCarrinho.push(produto);
					$scope.valorTotalDoCarrinho += ((produto.fields.valor_de_venda*produto.fields.quantidade_vendida)-produto.fields.desconto_combo);
					if(produto.fields.desconto_combo > 0){
						$scope.descontoComboFlag = true;
					}
				});
			};
		}, err => {
			$scope.erroTexto = "Ocorreu um erro enquanto tentávamos efetuar a operação desejada. Tente novamente.";
			$('#erroModal').modal();
		});
		$scope.produto_pk = undefined;
		$scope.buscarInput = "";
		$("#addModal").modal('hide');
		$("#buscarInput").trigger('focus');
	};

	$scope.buscar = function(input) {
		if(!(input=="")){
			$http.get('/api/consultaproduto/?pesquisa='+input).then(response => {
				let data = JSON.parse(response.data);
				if (data.length == 0){
					$scope.erroTexto = "Produto não encontrado.";
					$('#erroModal').modal();
				} else if (data.length > 1) {
					$scope.produtosBusca = [];
					angular.forEach(data, produto => {
						$scope.produtosBusca.push(produto);
					});
					$('#selectAddModal').modal();
				} else {
					data = data[0];
					$scope.produto_descricao = data.fields.descricao;
					$scope.produto_pk = data.pk;
					$scope.produto_valor_modal = data.fields.valor_de_venda;
					$('#addModal').modal();
				}
			}, err => {
				$scope.erroTexto = "Ocorreu um erro enquanto tentávamos efetuar a operação desejada. Tente novamente.";
				$('#erroModal').modal();
			});
		} else {
			$scope.finalizarVenda();
		};
	};

	$scope.buscaProdutosVendidos = function() {
		$http.get('/api/getprodutosvendaatual/').then(response => {
			let data = JSON.parse(response.data);
			$scope.itensNoCarrinho = [];
			$scope.valorTotalDoCarrinho = 0.00;
			$scope.descontoComboFlag = false;
			if (data.length == 0){
				$scope.caixaLivre = true;
			} else {
				$scope.caixaLivre = false;
				angular.forEach(data, (produto) => {
					$scope.itensNoCarrinho.push(produto);
					$scope.valorTotalDoCarrinho += ((produto.fields.valor_de_venda*produto.fields.quantidade_vendida)-produto.fields.desconto_combo);
					if(produto.fields.desconto_combo > 0){
						$scope.descontoComboFlag = true;
					}
				});
			};
		}, err => {
			$scope.erroTexto = "Ocorreu um erro enquanto tentávamos efetuar a operação desejada. Tente novamente.";
			$('#erroModal').modal();
		});
		$("#buscarInput").trigger('focus');
	};

	alteraProdutoOnCart = function(data){
		$http.post('/api/alteraprodutooncart/', data).then(response => {
			// Rotina para adicionar o produto à lista
			let data = JSON.parse(response.data);
			$scope.itensNoCarrinho = [];
			$scope.valorTotalDoCarrinho = 0.00;
			$scope.descontoComboFlag = false;
			if (data.length == 0){
				$scope.caixaLivre = true;
			} else {
				$scope.caixaLivre = false;
				angular.forEach(data, (produto) => {
					$scope.itensNoCarrinho.push(produto);
					$scope.valorTotalDoCarrinho += ((produto.fields.valor_de_venda*produto.fields.quantidade_vendida)-produto.fields.desconto_combo);
					if(produto.fields.desconto_combo > 0){
						$scope.descontoComboFlag = true;
					}
				});
			};
		}, err => {
			$scope.erroTexto = "Ocorreu um erro enquanto tentávamos efetuar a operação desejada. Tente novamente.";
			$('#erroModal').modal();
		});
	};

	$scope.menos = function(item){
		let data = {
			"qtd": -1,
			"produto_pk": item.pk,
			"venda_pk": $scope.venda_pk
		};
		alteraProdutoOnCart(data);
	};

	$scope.mais = function(item){
		let data = {
			"qtd": 1,
			"produto_pk": item.pk,
			"venda_pk": $scope.venda_pk
		};
		alteraProdutoOnCart(data);
	};

	$scope.selectProdBusca = function(produto){
		$('#selectAddModal').modal('hide');
		$scope.buscar(produto.fields.codigo_de_barras);
	};

	$scope.aplicaDesconto = function(){
		$scope.valorFinal = $scope.valorTotalDoCarrinho - $scope.descontoFinal;
	}

	$scope.finalizarVenda = function(){
		$scope.valorFinal = $scope.valorTotalDoCarrinho;
		$('#finalizarModal').modal();
	}

	$scope.finalizarVendaSubmit = function(){
		if($scope.descontoFinal == undefined){
			$scope.descontoFinal = 0;
		};
		if ($scope.pagamentoEscolhido == undefined) {
			$scope.finalizaMensagem = "Selecione a forma de pagamento";
			$scope.finalizaMensagensFlag = true;
		} else {
			$scope.finalizaMensagensFlag = false;
			data = {
				"venda_pk": $scope.venda_pk,
				"desconto": $scope.descontoFinal,
				"forma_de_pagamento": $scope.pagamentoEscolhido,
				"valor_total": $scope.valorTotalDoCarrinho
			};
			$http.post('/api/finalizarvenda/', data).then(response => {
				$('#finalizarModal').modal('hide');
				$scope.sucessoTexto = "Venda finalizada com sucesso.";
				$('#sucessoModal').modal();
			}, err => {
				$('#finalizarModal').modal('hide');
				$scope.erroTexto = "Houve um problema ao finalizar a venda.";
				$('#erroModal').modal();
			});
		};
	};

	$scope.cancelarVenda = function(){
		data = {
			"venda_pk": $scope.venda_pk
		};
		$http.post('/api/cancelarvenda/', data).then(response => {
			$scope.sucessoTexto = "Venda cancelada com sucesso.";
			$('#sucessoModal').modal();
		}, err => {
			$scope.erroTexto = "Não foi possível cancelar a venda.";
			$('#erroModal').modal();
		});
	}


});