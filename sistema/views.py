from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.contrib import messages
from .models import *
from .forms import *
import decimal, datetime
import pdb

@login_required
def dashboard(request):
	return render(request, "base.html")

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
	return render(request, "produtos.html", {"user": request.user, "produtos": produtos})

@login_required
def todosCombos(request):
	if (request.GET.get('search_box', None) == None):
		combos = Pack.objects.all().order_by('produto')
		paginator = Paginator(combos, 30)
		page = request.GET.get('page')
		combos = paginator.get_page(page)
	else:
		busca = request.GET.get('search_box', None)
		if busca.isnumeric():
			combos = Pack.objects.filter(produto__codigo_de_barras=busca)
		else:
			combos = Pack.objects.filter(produto__descricao__icontains=busca)
		paginator = Paginator(combos, 30)
		page = request.GET.get('page')
		combos = paginator.get_page(page)
	return render(request, "combos.html", {"user": request.user, "combos": combos})

@login_required
def addProdutos(request):
	if request.method == 'POST':
		form = produtoForm(request.POST)
		if form.is_valid():
			if(form.cleaned_data['este_produto_pode_ser_vendido_em_combo']):
				produto = Produto.objects.create(
					codigo_de_barras = form.cleaned_data['codigo_de_barras'],
					descricao = form.cleaned_data['descricao'],
					valor_de_venda = form.cleaned_data['valor_de_venda'],
					valor_de_compra = form.cleaned_data['valor_de_compra'],
					quantidade_em_estoque = form.cleaned_data['quantidade_em_estoque']
				)
				Pack.objects.create(
					produto = produto,
					quantidade_do_pack = form.cleaned_data['quantidade_do_combo'],
					valor_do_combro = form.cleaned_data['valor_do_combro']
				)
			else:
				produto = Produto.objects.create(
					codigo_de_barras = form.cleaned_data['codigo_de_barras'],
					descricao = form.cleaned_data['descricao'],
					valor_de_venda = form.cleaned_data['valor_de_venda'],
					valor_de_compra = form.cleaned_data['valor_de_compra'],
					quantidade_em_estoque = form.cleaned_data['quantidade_em_estoque']
				)
			messages.add_message(request, messages.SUCCESS, 'Produto adicionado com sucesso.')
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = produtoForm()
	return render(request, "addProdutos.html", {"user": request.user, "form": form})

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
	return render(request, 'detalheProduto.html', {"user": request.user, "form": form})

@login_required
def detalheCombo(request, pk):
	combo = Pack.objects.get(pk=pk)
	if request.method == 'POST':
		form = editPackForm(request.POST, instance=combo)
		if form.is_valid():
			combo = form.save()
			messages.add_message(request, messages.SUCCESS, 'Alteração salva com sucesso.')
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = editPackForm(instance=combo)
	return render(request, 'detalheCombo.html', {"user": request.user, "form": form})

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
	return render(request, 'addEstoque.html', {"user": request.user, "form": form})

@login_required
def todasVendas(request):
	dia = request.GET.get('dia')
	data_inicial = ''
	data_final = ''
	if dia == None or dia == 'hoje':
		data = datetime.date.today()
		vendas = Venda.objects.filter(data_e_hora__date=data).order_by('data_e_hora')
	elif dia == 'ontem':
		data = datetime.date.today() + datetime.timedelta(days=-1)
		vendas = Venda.objects.filter(data_e_hora__date=data).order_by('data_e_hora')
	elif dia == 'personalizado':
		if len(request.GET) == 3:
			holder_inicial = request.GET.get('inicial').split('-')
			holder_final = request.GET.get('final').split('-')
			data_inicial = datetime.date(int(holder_inicial[2]),int(holder_inicial[1]),int(holder_inicial[0])) # yyyy, mm, dd
			data_final = datetime.date(int(holder_final[2]),int(holder_final[1]),int(holder_final[0])) # yyyy, mm, dd
			vendas = Venda.objects.filter(data_e_hora__date__range=[data_inicial,data_final]).order_by('data_e_hora')
		else:
			vendas = Venda.objects.all().order_by('data_e_hora')
	total_dinheiro = decimal.Decimal('0.0')
	total_credito = decimal.Decimal('0.0')
	total_debito = decimal.Decimal('0.0')
	total_total = decimal.Decimal('0.0')
	for venda in vendas:
		if venda.forma_de_pagamento == 'DI':
			total_dinheiro += venda.valor_total
		elif venda.forma_de_pagamento == 'CR':
			total_credito += venda.valor_total
		elif venda.forma_de_pagamento == 'DE':
			total_debito += venda.valor_total
		total_total += venda.valor_total
	paginator = Paginator(vendas, 30)
	page = request.GET.get('page')
	vendas = paginator.get_page(page)
	return render(request, 'vendas.html', {"user": request.user, "vendas": vendas, "total_dinheiro": total_dinheiro, "total_credito": total_credito, "total_debito": total_debito, "total_total": total_total, 'dia': dia, "inicio": data_inicial,"fim": data_final})








