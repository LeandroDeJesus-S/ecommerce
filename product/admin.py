from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.StackedInline):
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [VariacaoInline]
    list_display = [
        'id', 'name', 'get_marketing_price_formatted', 
        'get_promotional_price_formatted',
    ]
    list_display_links = ['id', 'name']
    ordering = ['id']


class VariacaoAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock',]
    

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
