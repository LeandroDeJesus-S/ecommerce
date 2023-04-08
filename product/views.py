from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from perfil.models import Perfil
from django.contrib import messages
from .models import Produto, Variacao
from django.db.models import Q


class ListProduct(ListView):
    model = Produto
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


class ProductDetail(DetailView):
    model = Produto
    template_name = 'details.html'
    context_object_name = 'product_detail'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):            
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list_products'))
        variation_id = self.request.GET.get('vid')
        if not variation_id:
            messages.error(self.request, 'Error')
            return redirect(http_referer)
        
        variation = get_object_or_404(Variacao, id=variation_id)
        product = variation.product
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        
        if variation.stock < 1:
            messages.error(self.request, 'Estoque insuficiente.')
            return redirect(http_referer)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        was_add = True
        carrinho = self.request.session['carrinho']            
        if variation_id in carrinho:
            stock = variation.stock
            cart_quantity = carrinho[variation_id]['quantity']
            cart_quantity += 1
            if stock < cart_quantity:
                messages.warning(self.request, 'Estoque insuficiente.')
                cart_quantity = variation.stock
                was_add = False
                
            carrinho[variation_id]['quantity'] = cart_quantity
            carrinho[variation_id]['quantitative_price'] = cart_quantity * unit_price
            carrinho[variation_id]['promotional_quantitative_price'] = cart_quantity * promotional_unit_price
            
        
        else:
            carrinho[variation_id] = dict(
                product_id = product.id,
                product_name = product.name,
                variation_name = variation.name,
                variation_id = variation.id,
                unit_price = unit_price,
                promotional_unit_price = promotional_unit_price,
                quantity = 1,
                slug = product.slug,
                image = product.image.name if product.image else '',
                
            )
            quantity = carrinho[variation_id]['quantity']
            carrinho[variation_id]['quantitative_price'] = quantity * unit_price
            carrinho[variation_id]['promotional_quantitative_price'] = quantity * promotional_unit_price
        
        self.request.session.save()
        if was_add:
            messages.success(self.request, f'{product.name} adicionado ao carrinho.')
        return redirect(http_referer)


class RemoveToCart(View):
    def get(self, request, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list_products'))
        variation_id = self.request.GET.get('vid')
        carrinho = self.request.session.get('carrinho')
        if not variation_id:
            return redirect(http_referer)
        
        if not variation_id or not carrinho or variation_id not in carrinho:        
            return redirect(http_referer)

        product_name = carrinho[variation_id]['product_name']
        variation_name = carrinho[variation_id]['variation_name']
        messages.warning(
            self.request, 
            f'{product_name} {variation_name} removido.'
        )
        del self.request.session['carrinho'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'cart.html')


class PurchaseSummary(View):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:create')
        
        perfil = Perfil.objects.filter(user=self.request.user).exists()
        if not perfil:
            messages.error(self.request, 'Usuário não tem perfil.')
            return redirect('perfil:create')
        
        if not self.request.session.get('carrinho', {}):
            messages.error(self.request, 'Carrinho vazio.')
            return redirect('product:list_products')
        
        context = {
            'user': self.request.user,
            'cart': self.request.session.get('carrinho', {})
        }
        return render(self.request, 'salesummary.html', context)


class SearchProduct(ListProduct):
    def get_queryset(self, *args, **kwargs):
        search_field = self.request.GET.get('search_field') or self.request.session.get('search_fiedl')
        qs = super().get_queryset(*args, **kwargs)
        if not search_field: return qs
        
        self.request.session['search_fiedl'] = search_field
        
        qs = qs.filter(
            Q(name__icontains=search_field)|
            Q(short_description__icontains=search_field)|
            Q(long_description__icontains=search_field)
        )
        
        self.request.session.save()
        return qs
    