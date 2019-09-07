from django.urls import path, include
from apps.restful import views

app_name = 'restful'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order_create'),
    path('orders/create/', views.CreateOrderView.as_view(), name='order_create'),
    path('orders/accept/<int:pk>/', views.UpdateOrderView.as_view(), name='order_accept'),
    path('orders/update-status/<int:pk>/', views.UpdateOrderStatusView.as_view(), name='order_update_status'),

]
