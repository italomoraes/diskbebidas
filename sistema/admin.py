from django.contrib import admin

from .models import *

admin.site.register(Produto)
admin.site.register(Pack)
admin.site.register(Venda)
admin.site.register(ProdutoVendido)