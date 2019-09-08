from django.urls import path, include
from apps.restful import views

app_name = 'restful'

urlpatterns = [
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('client/orders/create/', views.CreateOrderView.as_view(), name='order_create'),
    path('driver/orders/', views.OrderListView.as_view(), name='order_list'),
    path('driver/orders/accept/<int:pk>/', views.UpdateOrderView.as_view(), name='order_accept'),
    path('driver/orders/update-status/<int:pk>/', views.UpdateOrderStatusView.as_view(), name='order_update_status'),

]
