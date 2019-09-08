from django.shortcuts import render
from django.views import generic
from rest_framework import generics, views, response, permissions
from rest_framework.generics import get_object_or_404

from apps.restful import serializers as restful_serializers
from apps.store import models as store_models


class OrderListView(generics.ListAPIView):
    serializer_class = restful_serializers.OrderSerializer

    def get_queryset(self):
        orders = store_models.Order.objects.filter(status=store_models.Order.NEW)
        return orders


class CreateOrderView(generics.CreateAPIView):
    serializer_class = restful_serializers.OrderCreateSerializer

    def get_queryset(self):
        return store_models.Order.objects.all()


class UpdateOrderView(generics.UpdateAPIView):
    serializer_class = restful_serializers.OrderUpdateSerializer

    def get_object(self):
        return get_object_or_404(store_models.Order, pk=self.kwargs.get('pk'))


class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = restful_serializers.OrderUpdateStatusSerializer

    def get_object(self):
        return get_object_or_404(store_models.Order, pk=self.kwargs.get('pk'))


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = restful_serializers.OrderSerializer

    def get_object(self):
        return get_object_or_404(store_models.Order, id=self.kwargs.get('pk'))
