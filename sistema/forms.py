from django import forms
from .models import *
from django.core.exceptions import ValidationError

def valida_codigo_de_barras_existe(codigo):
    produto = Produto.objects.filter(codigo_de_barras=codigo)
    if not produto.exists():
        raise ValidationError('Produto não cadastrado')

def valida_codigo_de_barras_nao_existe(codigo):
    produto = Produto.objects.filter(codigo_de_barras=codigo)
    if produto.exists():
        raise ValidationError('Produto já cadastrado')

class editPackForm(forms.ModelForm):
    produto = forms.CharField()
    quantidade_do_pack = forms.IntegerField(validators=[MinValueValidator(1,"Digite um valor maior que 1")])
    valor_do_combro = forms.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)

    produto.widget.attrs.update({'class': 'form-control col-3','style':'disabled: true;'})
    quantidade_do_pack.widget.attrs.update({'class': 'form-control col-3'})
    valor_do_combro.widget.attrs.update({'class': 'form-control col-3'})

    class Meta:
        model = Pack
        fields = ('__all__')

class editProdutoForm(forms.ModelForm):
    codigo_de_barras = forms.CharField(max_length=13)
    descricao = forms.CharField(max_length=200)
    valor_de_venda = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    valor_de_compra = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    quantidade_em_estoque = forms.IntegerField(validators=[MinValueValidator(0)])

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    descricao.widget.attrs.update({'class': 'form-control col-12'})
    valor_de_venda.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3'})
    quantidade_em_estoque.widget.attrs.update({'class': 'form-control col-3'})

    class Meta:
        model = Produto
        fields = ('__all__')


class produtoForm(forms.Form):
    codigo_de_barras = forms.CharField(max_length=13, validators=[valida_codigo_de_barras_nao_existe])
    descricao = forms.CharField(max_length=200)
    valor_de_compra = forms.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    valor_de_venda = forms.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2)
    quantidade_em_estoque = forms.IntegerField(validators=[MinValueValidator(0)])
    este_produto_pode_ser_vendido_em_combo = forms.BooleanField(required=False)
    quantidade_do_combo = forms.IntegerField(validators=[MinValueValidator(0)], required=False)
    valor_do_combro = forms.DecimalField(validators=[MinValueValidator(0)], max_digits=7, decimal_places=2, required=False)

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    descricao.widget.attrs.update({'class': 'form-control col-12'})
    valor_de_venda.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3'})
    quantidade_em_estoque.widget.attrs.update({'class': 'form-control col-3'})
    este_produto_pode_ser_vendido_em_combo.widget.attrs.update({'class': 'form-control'})
    quantidade_do_combo.widget.attrs.update({'class': 'form-control col-3'})
    valor_do_combro.widget.attrs.update({'class': 'form-control col-3'})


class addEstoqueForm(forms.Form):
    codigo_de_barras = forms.CharField(max_length=13, validators=[valida_codigo_de_barras_existe])
    quantidade_adicional = forms.IntegerField(validators=[MinValueValidator(0)])
    valor_de_compra = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    lucro_em_porcentagem = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3', 'placeholder': 'R$'})
    lucro_em_porcentagem.widget.attrs.update({'class': 'form-control col-3','placeholder': '%'})
    quantidade_adicional.widget.attrs.update({'class': 'form-control col-3'})


