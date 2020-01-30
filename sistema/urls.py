from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('produtos/', views.todosProdutos, name='todosProdutos'),
    path('produtos/<pk>/', views.detalheProduto, name='detalheProduto'),
    path('addProdutos/', views.addProdutos, name='addProdutos'),
    path('addEstoque/', views.addEstoque, name='addEstoque'),
    path('addEstoque/pack/<pk>/', views.addEstoquePack, name='addEstoquePack'),
    path('addCombo/', views.addCombo, name='addCombo'),
    path('vendas/', views.todasVendas, name='todasVendas'),
    path('vendas/<pk>/', views.detalheVenda, name='detalheVenda'),
    path('combos/', views.todosCombos, name='todosCombos'),
    path('combos/<pk>/', views.detalheCombo, name='detalheCombo'),
    path('pdv/', views.clicaPDV, name='clicaPDV'),
    path('pdv/<pk>/', views.pdv, name='pdv'),
    path('api/consultaproduto/', views.consultaProdutoApi, name='consultaProdutoApi'),
    path('api/addprodutotocart/', views.addProdutoToCart, name='addProdutoToCart'),
    path('api/getprodutosvendaatual/', views.getProdutosVendaAtual, name='getProdutosVendaAtual'),
    path('api/alteraprodutooncart/', views.alteraProdutoOnCart, name='alteraProdutoOnCart'),
    path('api/finalizarvenda/', views.finalizarVenda, name='finalizarvenda'),
    path('api/cancelarvenda/', views.cancelarVenda, name='cancelarVenda')
]