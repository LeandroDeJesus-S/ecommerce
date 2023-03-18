from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pay/<int:pk>/', views.Payment.as_view(), name='pay'),
    path('save-order/', views.SaveOrder.as_view(), name='save_order'),
    path('list-order/', views.ListOrder.as_view(), name='list_order'),
    path('order-detail/<int:pk>', views.Detail.as_view(), name='detail'),
]
