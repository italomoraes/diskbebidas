from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator
from django.contrib import messages
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
import decimal, datetime, json, math
import pdb

@login_required
def dashboard(request):
	return redirect('clicaPDV')

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
	return render(request, "combos.html", {"pagina": "todosCombos", "user": request.user, "combos": combos})

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
def detalheCombo(request, pk):
	combo = Pack.objects.get(pk=pk)
	produto = combo.produto
	if request.method == 'POST':
		form = editPackForm(request.POST, instance=combo)
		if form.is_valid():
			combo = form.save()
			messages.add_message(request, messages.SUCCESS, 'Alteração salva com sucesso.')
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = editPackForm(instance=combo)
	return render(request, 'detalheCombo.html', {"pagina": "todosCombos", "user": request.user, "form": form, "produto": produto})

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
			if Pack.objects.filter(produto__codigo_de_barras=form.cleaned_data['codigo_de_barras']).exists():
				return redirect('addEstoquePack', pk=produto.pk)
			messages.add_message(request, messages.SUCCESS, 'Entrada cadastrada com sucesso para '+produto.descricao)
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = addEstoqueForm()
	return render(request, 'addEstoque.html', {"pagina": "addEstoque", "user": request.user, "form": form})

@login_required
def addEstoquePack(request, pk):
	if request.method == 'POST':
		form = addEstoquePackForm(request.POST)
		if form.is_valid():
			pack = Pack.objects.get(produto__pk=pk)
			pack.valor_do_combro = form.cleaned_data['valor_do_combro']
			pack.save()
			messages.add_message(request, messages.SUCCESS, 'Entrada cadastrada com sucesso para '+pack.produto.descricao)
			return redirect('addEstoque')
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		produto = Produto.objects.get(pk=pk)
		pack = Pack.objects.get(produto=produto)
		form = addEstoquePackForm()
		valor_sugerido = produto.valor_de_venda*pack.quantidade_do_pack
	return render(request, 'addEstoquePack.html', {"pagina": "addEstoque", "user": request.user, "form": form, "pack": pack, "produto": produto, "valor_sugerido": valor_sugerido})

@login_required
def addCombo(request):
	if request.method == 'POST':
		form = addComboForm(request.POST)
		if form.is_valid():
			combo = form.save()
			messages.add_message(request, messages.SUCCESS, 'Entrada cadastrada com sucesso para '+combo.produto.descricao)
		else:
			messages.add_message(request, messages.ERROR, 'Formulário inválido')
	else:
		form = addComboForm()
	return render(request, 'addCombo.html', {"pagina": "addCombo", "user": request.user, "form": form})


@login_required
def todasVendas(request):
	dia = request.GET.get('dia')
	data_inicial = ''
	data_final = ''
	if dia == None or dia == 'hoje':
		data = datetime.date.today()
		vendas = Venda.objects.filter(data_e_hora__date=data).filter(finalizado=True).order_by('-data_e_hora')
	elif dia == 'ontem':
		data = datetime.date.today() + datetime.timedelta(days=-1)
		vendas = Venda.objects.filter(data_e_hora__date=data).filter(finalizado=True).order_by('-data_e_hora')
	elif dia == 'personalizado':
		if len(request.GET) == 3:
			holder_inicial = request.GET.get('inicial').split('-')
			holder_final = request.GET.get('final').split('-')
			data_inicial = datetime.date(int(holder_inicial[2]),int(holder_inicial[1]),int(holder_inicial[0])) # yyyy, mm, dd
			data_final = datetime.date(int(holder_final[2]),int(holder_final[1]),int(holder_final[0])) # yyyy, mm, dd
			vendas = Venda.objects.filter(data_e_hora__date__range=[data_inicial,data_final]).order_by('data_e_hora')
		else:
			vendas = Venda.objects.all().filter(finalizado=True).order_by('-data_e_hora')
	total_dinheiro = decimal.Decimal('0.0')
	total_credito = decimal.Decimal('0.0')
	total_debito = decimal.Decimal('0.0')
	total_total = decimal.Decimal('0.0')
	for venda in vendas:
		if venda.forma_de_pagamento == 'DI':
			total_dinheiro += (venda.valor_total-venda.desconto)
		elif venda.forma_de_pagamento == 'CR':
			total_credito += (venda.valor_total-venda.desconto)
		elif venda.forma_de_pagamento == 'DE':
			total_debito += (venda.valor_total-venda.desconto)
		total_total += (venda.valor_total-venda.desconto)
	paginator = Paginator(vendas, 30)
	page = request.GET.get('page')
	vendas = paginator.get_page(page)
	return render(request, 'vendas.html', {"pagina": "todasVendas", "user": request.user, "vendas": vendas, "total_dinheiro": total_dinheiro, "total_credito": total_credito, "total_debito": total_debito, "total_total": total_total, 'dia': dia, "inicio": data_inicial,"fim": data_final})

@login_required
def detalheVenda(request, pk):
	venda_obj = Venda.objects.get(pk=pk)
	valor_final = venda_obj.valor_total - venda_obj.desconto
	produtos_vendidos = ProdutoVendido.objects.filter(venda=venda_obj)
	valor_de_custo = 0;
	for produto in produtos_vendidos:
		valor_de_custo += (produto.valor_de_compra*produto.quantidade_vendida)
	lucro_moeda = valor_final - valor_de_custo
	venda = {
		'valor_final': valor_final,
		'lucro_moeda': lucro_moeda,
		'lucro_porcentagem': (lucro_moeda/valor_final)*100
	}
	return render(request, 'detalheVenda.html', {"pagina": "todasVendas", "user": request.user, "venda_obj": venda_obj, "venda": venda, "produtos_vendidos": produtos_vendidos})

@login_required
def clicaPDV(request):
	venda = Venda.objects.latest('pk')
	if venda.finalizado:
		venda_atual = Venda.objects.create(
			valor_total = decimal.Decimal(0.0),
			forma_de_pagamento = 'DI',
			desconto = decimal.Decimal(0)
		)
	else:
		venda_atual = venda
	return redirect('pdv', pk=venda_atual.pk)

@login_required
def pdv(request, pk):
	venda = Venda.objects.get(pk=pk)
	return render(request, 'pdv.html', {"pagina": "pdv", "user": request.user, "pagina": "pdv", "venda": venda})


# Api Views

@login_required
def consultaProdutoApi(request):
	pesquisa = request.GET.get('pesquisa')
	if pesquisa.isnumeric() and len(pesquisa) >= 4:
		produtos = Produto.objects.filter(codigo_de_barras=pesquisa)
	else:
		produtos = Produto.objects.filter(descricao__icontains=pesquisa)
	return JsonResponse(serializers.serialize("json", produtos), safe=False)

@login_required
def getProdutosVendaAtual(request):
	venda = Venda.objects.latest('pk')
	produtos_vendidos = ProdutoVendido.objects.filter(venda=venda)
	return JsonResponse(serializers.serialize("json", produtos_vendidos), safe=False)

@login_required
@csrf_exempt
def addProdutoToCart(request):
	data = json.loads(request.body)
	produto = Produto.objects.get(pk=data.get('produto_pk'))
	venda = Venda.objects.get(pk=data.get('venda_pk'))
	produto_sendo_vendido = ProdutoVendido.objects.filter(venda=venda).filter(codigo_de_barras=produto.codigo_de_barras)
	quantidade = int(data.get('qtd'))
	if produto_sendo_vendido.exists():
		produto_vendido = produto_sendo_vendido.first()
		produto_vendido.quantidade_vendida += quantidade
	else:
		produto_vendido = ProdutoVendido.objects.create(
			venda = venda,
			codigo_de_barras = produto.codigo_de_barras,
			descricao = produto.descricao,
			valor_de_venda = produto.valor_de_venda,
			valor_de_compra = produto.valor_de_compra,
			quantidade_vendida = quantidade
		)
	combo = Pack.objects.filter(produto__codigo_de_barras=produto_vendido.codigo_de_barras)
	if combo.exists() and produto_vendido.quantidade_vendida >= combo.quantidade_do_pack:
		combo = combo.first()
		numero_de_combos = math.floor(produto_vendido.quantidade_vendida/combo.quantidade_do_pack)
		produto_vendido.desconto_combo = numero_de_combos*((combo.quantidade_do_pack*produto_vendido.valor_de_venda)-combo.valor_do_combro)
	else:
		produto_vendido.desconto_combo = 0
	produto_vendido.save()
	produtos_vendidos = ProdutoVendido.objects.filter(venda=venda)
	return JsonResponse(serializers.serialize("json", produtos_vendidos), safe=False)


@login_required
@csrf_exempt
def alteraProdutoOnCart(request):
	data = json.loads(request.body)
	quantidade = int(data.get('qtd'))
	produto_sendo_alterado = ProdutoVendido.objects.get(pk=data.get('produto_pk'))
	combo = Pack.objects.filter(produto__codigo_de_barras=produto_sendo_alterado.codigo_de_barras)
	produto_sendo_alterado.quantidade_vendida += quantidade
	if produto_sendo_alterado.quantidade_vendida == 0:
		produto_sendo_alterado.delete()
	elif combo.exists() and produto_sendo_alterado.quantidade_vendida >= combo.quantidade_do_pack:
		ombo = combo.first()
		numero_de_combos = math.floor(produto_sendo_alterado.quantidade_vendida/combo.quantidade_do_pack)
		produto_sendo_alterado.desconto_combo = numero_de_combos*((combo.quantidade_do_pack*produto_sendo_alterado.valor_de_venda)-combo.valor_do_combro)
		produto_sendo_alterado.save()
	else:
		produto_sendo_alterado.desconto_combo = 0
		produto_sendo_alterado.save()
	produtos_vendidos = ProdutoVendido.objects.filter(venda__pk=data.get('venda_pk'))
	return JsonResponse(serializers.serialize("json", produtos_vendidos), safe=False)


@login_required
@csrf_exempt
def finalizarVenda(request):
	data = json.loads(request.body)
	venda = Venda.objects.get(pk=data.get('venda_pk'))
	venda.desconto = decimal.Decimal(data.get('desconto'))
	venda.forma_de_pagamento = data.get('forma_de_pagamento')
	venda.valor_total = data.get('valor_total')
	venda.data_e_hora = datetime.datetime.now()
	produtos_vendidos = ProdutoVendido.objects.filter(venda=venda)
	for produto in produtos_vendidos:
		produto_a_subtrair = Produto.objects.get(codigo_de_barras=produto.codigo_de_barras)
		produto_a_subtrair.quantidade_em_estoque -= produto.quantidade_vendida
		produto_a_subtrair.save()
	venda.finalizado = True
	venda.save()
	return HttpResponse(status=200)


@login_required
@csrf_exempt
def cancelarVenda(request):
	data = json.loads(request.body)
	produtos = ProdutoVendido.objects.filter(venda__pk=data.get('venda_pk'))
	for produto in produtos:
		produto.delete()
	return HttpResponse(status=200)

