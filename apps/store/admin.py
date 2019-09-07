from django.contrib import admin
from apps.store import models as store_models


class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'total_cost', 'customer', 'driver', 'created_at', ]


admin.site.register(store_models.Order, OrderAdmin)
