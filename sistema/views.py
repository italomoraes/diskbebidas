from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from .forms import *
import pdb

@login_required
def index(request):
	return render(request, "base.html", {"pagina": "index"})

@login_required
def todosProdutos(request):
	if (request.GET.get('search_box', None) == None):
		produtos = Produto.objects.all().order_by('descricao')
		paginator = Paginator(produtos, 30)
		page = request.GET.get('page')
		produtos = paginator.get_page(page)
	else:
		busca = request.GET.get('search_box', None)
		if busca.isnumeric():
			produtos = Produto.objects.filter(codigo_de_barras=busca)
		else:
			produtos = Produto.objects.filter(descricao__icontains=busca)
		paginator = Paginator(produtos, 30)
		page = request.GET.get('page')
		produtos = paginator.get_page(page)
	return render(request, "produtos.html", {"pagina": "todosProdutos", "user": request.user, "produtos": produtos})

@login_required
def addProdutos(request):
	if request.method == 'POST':
		form = addProdutoForm(request.POST)
		if form.is_valid():
			produto = form.save()
			messages.add_message(request, messages.SUCCESS, 'Produto adicionado com sucesso.')
			return render(request, "addProdutos.html", {"pagina": "addProdutos", "user": request.user, "form": form})
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
			return render(request, "addProdutos.html", {"pagina": "addProdutos", "user": request.user, "form": form})
	else:
		form = addProdutoForm()
		return render(request, "addProdutos.html", {"pagina": "addProdutos", "user": request.user, "form": form})

@login_required
def detalheProduto(request, pk):
	produto = Produto.objects.get(pk=pk)
	if request.method == 'POST':
		form = editProdutoForm(request.POST, instance=produto)
		if form.is_valid():
			produto = form.save()
			messages.add_message(request, messages.SUCCESS, 'Alteração salva com sucesso.')
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = editProdutoForm(instance=produto)
	return render(request, 'detalheProduto.html', {"pagina": "todosProdutos", "user": request.user, "form": form})

@login_required
def addEstoque(request):
	if request.method == 'POST':
		form = addEstoqueForm(request.POST)
		if form.is_valid():
			codigo_de_barras = form.cleaned_data.get('codigo_de_barras')
			custo_novo = form.cleaned_data['valor_de_compra']
			lucro = form.cleaned_data['lucro_em_porcentagem']
			quantidade_adicional = form.cleaned_data['quantidade_adicional']
			produto = Produto.objects.get(codigo_de_barras=codigo_de_barras)
			custo_antigo = produto.valor_de_compra
			quantidade_em_estoque = produto.quantidade_em_estoque
			custo_real = ((quantidade_em_estoque*custo_antigo)+(quantidade_adicional*custo_novo))/(quantidade_adicional+quantidade_em_estoque)
			produto.valor_de_compra = custo_real
			produto.quantidade_em_estoque = quantidade_em_estoque + quantidade_adicional
			produto.valor_de_venda = custo_real*(1+(lucro/100))
			produto.save()
			messages.add_message(request, messages.SUCCESS, 'Entrada cadastrada com sucesso para '+produto.descricao)
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = addEstoqueForm()
	return render(request, 'addEstoque.html', {"pagina": "addEstoque", "user": request.user, "form": form})


@login_required
def todasVendas(request):
	vendas = Venda.objects.all().order_by('data_e_hora')
	paginator = Paginator(vendas, 30)
	page = request.GET.get('page')
	vendas = paginator.get_page(page)
	return render(request, 'vendas.html', {"pagina": "todasVendas", "user": request.user, "vendas": vendas})








