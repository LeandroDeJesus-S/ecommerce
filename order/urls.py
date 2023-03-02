from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Payment.as_view(), name='pay'),
    path('close-order/', views.CloseOrder.as_view(), name='close_order'),
    path('order-detail/<int:pk>', views.Detail.as_view(), name='detail'),
]
