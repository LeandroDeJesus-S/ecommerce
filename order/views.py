from django.shortcuts import render, redirect
from utils import functions
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages

from product.models import Variacao
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models


class LoginRequiredBaseMixin(LoginRequiredMixin, View):
    login_url = 'perfil:create'
    permission_denied_message = 'Você não tem permissão para acessar esta pagina'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs 


class Payment(LoginRequiredBaseMixin, DetailView):
    template_name = 'topay.html'
    model = models.Pedido
    pk_url_kwarg = 'pk'


class SaveOrder(Payment):
    template_name = 'topay.html'
    
    def get(self, *args, **kwargs):
        context = {}
        render_ = render(self.request, self.template_name, context)
        if not self.request.user.is_authenticated:
            return redirect('perfil:create')
        
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Carrinho vazio.')
            return render_
        
        cart = self.request.session.get('carrinho')
        products_vars = list(cart.keys())
        db_var = list(Variacao.objects.filter(id__in=products_vars))
        
        enough = True
        for var in db_var:
            vid = str(var.id)
            stock = var.stock
            cart_quantity = cart[vid]['quantity']
            unt_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']

            if stock < cart_quantity:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unt_price
                cart[vid]['promotional_quantitative_price'] = stock * promotional_unit_price
                enough = False
        
        if not enough:
            messages.warning(
                self.request, 'Alguns itens foram reduzidos por estoque insuficiente.'
                              'verifique os itens abaixo antes de continuar.'
            )
            
            self.request.session.save()
            return redirect(self.request.META.get('http_referer', 
                                                  'product:purchase_summary'))
        
        cart_total_quantity = functions.get_cart_quantity(cart)
        cart_total_value = functions.amount(cart)
        
        order = models.Pedido(
            user=self.request.user, 
            total=cart_total_value, 
            total_quantity=cart_total_quantity,
            status='C'
        )
        order.save()
        
        models.ItemPedido.objects.bulk_create(
                [models.ItemPedido(
                    order = order,
                    product = v['product_name'],
                    product_id = v['product_id'],
                    variation = v['variation_name'],
                    variation_id = v['variation_id'],
                    price = v['quantitative_price'],
                    promotional_price = v['promotional_quantitative_price'],
                    quantity = v['quantity'],
                    image = v['image'],
                ) for v in cart.values()]
            )
        del self.request.session['carrinho']
        return redirect('order:pay', pk=order.pk)

class Detail(LoginRequiredBaseMixin, DetailView):
    login_url = 'perfil:create'
    model = models.Pedido
    template_name = 'detail.html'
    ordering = ['-id']


class ListOrder(LoginRequiredBaseMixin, ListView):
    login_url = 'perfil:create'
    model = models.Pedido
    context_object_name = 'orders'
    template_name = 'list_orders.html'
    paginate_by = 10
    ordering = ['-id']
