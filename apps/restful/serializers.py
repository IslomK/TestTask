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

    def to_representation(self, instance):
        kwargs = {
            'order_id': instance.id,
            'customer_full_name': instance.customer.user.get_full_name(),
            'customer_phone': instance.customer.user.phone,
            'created_at': instance.created_at,
            'status': instance.status
        }
        if instance.status != store_models.Order.NEW:
            kwargs.update({
                'driver_full_name': instance.driver.user.get_full_name(),
                'driver_phone': instance.driver.user.phone,
                'car_number': instance.driver.car_number,
            })
        if instance.status == store_models.Order.COMPLETED:
            kwargs.update({
                'total_cost': instance.total_cost
            })

        return kwargs


class OrderCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=250, write_only=True)
    last_name = serializers.CharField(max_length=250, write_only=True)
    phone = serializers.CharField(max_length=250, write_only=True)
    car_number = serializers.CharField(max_length=250, required=False, read_only=True)

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
        return OrderSerializer.to_representation(OrderSerializer, instance)


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
        return OrderSerializer.to_representation(OrderSerializer, instance)

    def validate_phone(self, value):
        if account_models.User.objects.filter(phone=value, user_type=account_models.User.CLIENT).exists():
            raise serializers.ValidationError("Client is registered with this number")
        return value


class OrderUpdateStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = store_models.Order
        fields = ['status', 'total_cost']

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        total_cost = validated_data.get('total_cost', None)

        if status == store_models.Order.COMPLETED:
            if not total_cost:
                raise serializers.ValidationError({
                    "total_cost": "Can not update status to completed without total_cost field"
                })
            instance.total_cost = total_cost

        instance.status = status
        instance.save()
        instance.refresh_from_db()
        return instance

    def to_representation(self, instance):
        return OrderSerializer.to_representation(OrderSerializer, instance)
