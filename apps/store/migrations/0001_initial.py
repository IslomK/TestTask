# Generated by Django 2.2.5 on 2019-09-05 17:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_cost', models.FloatField()),
                ('status', models.CharField(choices=[('new', 'New'), ('driver_accepted', 'Accepted by driver'), ('driver_arrived', 'Driver arrived'), ('client_in_car', 'Client is in car'), ('completed', 'Order is completed')], max_length=255)),
            ],
        ),
    ]