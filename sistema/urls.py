from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produtos/', views.todosProdutos, name='todosProdutos'),
    path('produtos/<pk>/', views.detalheProduto, name='detalheProduto'),
    path('addProdutos/', views.addProdutos, name='addProdutos'),
    path('addEstoque/', views.addEstoque, name='addEstoque'),
    path('vendas/', views.todasVendas, name='todasVendas')
]