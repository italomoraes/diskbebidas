from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('produtos/', views.todosProdutos, name='todosProdutos'),
    path('produtos/<pk>/', views.detalheProduto, name='detalheProduto'),
    path('addProdutos/', views.addProdutos, name='addProdutos'),
    path('addEstoque/', views.addEstoque, name='addEstoque'),
    path('vendas/', views.todasVendas, name='todasVendas'),
    path('combos/', views.todosCombos, name='todosCombos'),
    path('combos/<pk>/', views.detalheCombo, name='detalheCombo'),
]