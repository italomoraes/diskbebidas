from django import forms
from .models import *
from django.core.exceptions import ValidationError

def valida_codigo_de_barras(codigo):
    produto = Produto.objects.filter(codigo_de_barras=codigo)
    if not produto.exists():
        raise ValidationError('Produto não cadastrado')

class addProdutoForm(forms.ModelForm):
    codigo_de_barras = forms.CharField(max_length=13)
    descricao = forms.CharField()
    valor_de_compra = forms.DecimalField()
    valor_de_venda = forms.DecimalField()
    quantidade_em_estoque = forms.IntegerField()

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    descricao.widget.attrs.update({'class': 'form-control col-12'})
    valor_de_venda.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3'})
    quantidade_em_estoque.widget.attrs.update({'class': 'form-control col-3'})

    class Meta:
    	model = Produto
    	fields = ('__all__')


class editProdutoForm(forms.ModelForm):
    codigo_de_barras = forms.CharField(max_length=13)
    descricao = forms.CharField()
    valor_de_compra = forms.DecimalField()
    valor_de_venda = forms.DecimalField()
    quantidade_em_estoque = forms.IntegerField()

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    descricao.widget.attrs.update({'class': 'form-control col-12'})
    valor_de_venda.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3'})
    quantidade_em_estoque.widget.attrs.update({'class': 'form-control col-3'})

    class Meta:
        model = Produto
        fields = ('__all__')


class addEstoqueForm(forms.Form):
    codigo_de_barras = forms.CharField(max_length=13, validators=[valida_codigo_de_barras])
    quantidade_adicional = forms.IntegerField(validators=[MinValueValidator(0)])
    valor_de_compra = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)
    lucro_em_porcentagem = forms.DecimalField(validators=[MinValueValidator(0)],max_digits=7, decimal_places=2)

    codigo_de_barras.widget.attrs.update({'class': 'form-control col-3'})
    valor_de_compra.widget.attrs.update({'class': 'form-control col-3', 'placeholder': 'R$'})
    lucro_em_porcentagem.widget.attrs.update({'class': 'form-control col-3','placeholder': '%'})
    quantidade_adicional.widget.attrs.update({'class': 'form-control col-3'})


