from django.db import models
from django.utils import timezone


class Order(models.Model):
    NEW = 'new'
    DRIVER_ACCEPTED = 'driver_accepted'
    DRIVER_ARRIVED = 'driver_arrived'
    CLIENT_IN_CAR = 'client_in_car'
    COMPLETED = 'completed'

    STATUS_TYPES = (
        (NEW, 'New'),
        (DRIVER_ACCEPTED, 'Accepted by driver'),
        (DRIVER_ARRIVED, 'Driver arrived'),
        (CLIENT_IN_CAR, 'Client is in car'),
        (COMPLETED, 'Order is completed')
    )

    created_at = models.DateTimeField(default=timezone.now)
    total_cost = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_TYPES, null=True)
    customer = models.ForeignKey('account.ClientProfile', on_delete=models.CASCADE, related_name='orders', null=True,
                                 blank=True)
    driver = models.ForeignKey('account.DriverProfile', on_delete=models.CASCADE, related_name='orders', null=True,
                               blank=True)
