from django.contrib import admin
from apps.account import models as account_models
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(account_models.User)
class UserAdmin(DjangoUserAdmin, admin.ModelAdmin):
    fieldsets = (
        ('Main', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type', 'phone', 'email', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'first_name', 'last_name', 'user_type',),
        }),
    )
    list_display = ('get_fullname', 'is_staff', 'user_type', 'date_joined', )
    list_filter = ('user_type',)
    search_fields = ('email', 'first_name', 'last_name', 'phone',)
    ordering = ('email',)

    @staticmethod
    def get_fullname(obj):
        if obj.first_name or obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name)
        return "{}".format(obj.username)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'car_number']


class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', ]


admin.site.register(account_models.DriverProfile, DriverProfileAdmin)
admin.site.register(account_models.ClientProfile, ClientProfileAdmin)

