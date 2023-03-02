from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Produto, Variacao
from pprint import pprint


class ListProduct(ListView):
    model = Produto
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    model = Produto
    template_name = 'details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()
            
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
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
            
        carrinho = self.request.session['carrinho']            
        if variation_id in carrinho:
            stock = variation.stock
            cart_quantity = carrinho[variation_id]['quantity']
            cart_quantity += 1
            if stock < cart_quantity:  # TODO: resolver msgs duplicadas
                messages.warning(self.request, 'Estoque insuficiente.')
                cart_quantity = variation.stock
                
            carrinho[variation_id]['quantity'] = cart_quantity
            carrinho[variation_id]['quantitative_price'] = cart_quantity * unit_price
            carrinho[variation_id]['promotional_quantitative_price'] = cart_quantity * promotional_unit_price
            
        else:
            carrinho[variation_id] = dict(
                product_id = product.id,
                product_name = product.name,
                variation_name = variation.name,
                variation_id = variation.id,
                unit_price = variation.price,
                promotional_unit_price = variation.promotional_price,
                quantity = 1,
                slug = product.slug,
                image = product.image.name if product.image else '',
                
            )
            quantity = carrinho[variation_id]['quantity']
            carrinho[variation_id]['quantitative_price'] = quantity * unit_price
            carrinho[variation_id]['promotional_quantitative_price'] = quantity * promotional_unit_price
        
        self.request.session.save()
        pprint(carrinho)
        messages.success(self.request, f'{product.name} adicionado ao carrinho.')
        return redirect(http_referer)


class RemoveToCart(View):
    def get(self, request, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('product:list'))
        variation_id = self.request.GET.get('vid')
        if not variation_id:
            return redirect(http_referer)
        carrinho = self.request.session.get('carrinho')
        if not carrinho:        
            return redirect(http_referer)
        
        if variation_id not in carrinho:
            return redirect(http_referer)
        carrinho_product = carrinho[variation_id]
        messages.success(
            self.request, 
            f'{carrinho_product["product_name"]} {carrinho_product["variation_name"]} removido.'
        )
        del self.request.session['carrinho'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'cart.html')


class Finalize(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Finalize')
