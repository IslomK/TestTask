from apps.account import models as account_models
from apps.store import models as store_models
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = account_models.ClientProfile
        fields = ['first_name', 'last_name', 'phone']

    @staticmethod
    def get_first_name(obj):
        return obj.user.first_name

    @staticmethod
    def get_last_name(obj):
        return obj.user.last_name

    @staticmethod
    def get_phone(obj):
        return obj.user.phone


class DriverSerializer(ClientSerializer):

    class Meta:
        model = account_models.DriverProfile
        fields = ['first_name', 'last_name', 'phone', 'car_number']

    def validate_car_number(self, val):
        if account_models.DriverProfile.objects.filter(car_number=val).exists():
            raise serializers.ValidationError('Driver with this car number already exists')
        return val


class OrderSerializer(serializers.ModelSerializer):
    customer = ClientSerializer()
    driver = DriverSerializer()

    class Meta:
        model = store_models.Order
        fields = ['created_at', 'total_cost', 'status', 'customer', 'driver', ]


class OrderCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=250, write_only=True)
    last_name = serializers.CharField(max_length=250, write_only=True)
    phone = serializers.CharField(max_length=250, write_only=True)
    car_number = serializers.CharField(max_length=250, required=False, write_only=True)

    class Meta:
        model = store_models.Order
        fields = ['first_name', 'last_name', 'phone', 'car_number', ]

    def create(self, validated_data):
        phone = validated_data.get("phone", None)
        user = account_models.User.objects.filter(phone=phone)
        if user.exists():
            user = user.first()
        else:
            user = account_models.User.objects.create(**validated_data, password=phone, username=phone,
                                                      user_type=account_models.User.CLIENT)
        client = account_models.ClientProfile.objects.create(user=user)
        order = store_models.Order.objects.create(customer=client, status=store_models.Order.NEW)
        return order

    def to_representation(self, instance):
        return {
            'order_id': instance.id,
            'customer_full_name': instance.customer.user.get_full_name(),
            'status': instance.status
        }


class OrderUpdateSerializer(OrderCreateSerializer):
    car_number = serializers.CharField(max_length=250, required=True, write_only=True)

    def update(self, instance, validated_data):
        car_number = validated_data.pop('car_number', None)
        phone = validated_data.get("phone", None)
        user = account_models.User.objects.filter(phone=phone, user_type=account_models.User.DRIVER)

        if user.exists():
            user = user.first()
        else:
            user = account_models.User.objects.create(**validated_data, password=phone, username=phone,
                                                      user_type=account_models.User.DRIVER)

        driver = account_models.DriverProfile.objects.create(user=user, car_number=car_number)
        instance.driver = driver
        instance.status = store_models.Order.DRIVER_ACCEPTED
        instance.save()
        instance.refresh_from_db()

        return instance

    def to_representation(self, instance):
        return {
            'order_id': instance.id,
            'customer_full_name': instance.customer.user.get_full_name(),
            'driver_full_name': instance.driver.user.get_full_name(),
            'car_number': instance.driver.car_number,
            'status': instance.status
        }

    def validate_phone(self, value):
        if account_models.User.objects.filter(phone=value, user_type=account_models.User.CLIENT).exists():
            raise serializers.ValidationError("Client is registered with this number")
        return value


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.Order
        fields = ['status', ]

    def to_representation(self, instance):
        return {
            'order_id': instance.id,
            'customer_full_name': instance.customer.user.get_full_name(),
            'driver_full_name': instance.driver.user.get_full_name(),
            'car_number': instance.driver.car_number,
            'status': instance.status
        }
