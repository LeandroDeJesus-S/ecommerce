from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('', views.ListProduct.as_view(), name='list'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('remove-to-cart/', views.RemoveToCart.as_view(), name='remove_to_cart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('finalize/', views.Finalize.as_view(), name='finalize'),
    path('<str:slug>/', views.ProductDetail.as_view(), name='details'),
]
