# Generated by Django 2.2.3 on 2020-04-30 20:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('restaurant_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('working_hours', models.CharField(max_length=100)),
                ('cost_for_two', models.CharField(max_length=100)),
                ('contact_number', models.CharField(help_text='Contact Number of the restaurant owner', max_length=100, null=True)),
            ],
            options={
                'db_table': 'Restaurant',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('uuid', models.CharField(default='', max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('mobile_num', models.CharField(max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField()),
                ('date_time', models.DateTimeField(auto_now=True, null=True)),
                ('order_description', models.CharField(max_length=1000)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('payment_method', models.CharField(choices=[('Cash On Delivery', 'COD'), ('Online-UPI', 'UPI'), ('Online-Paytm', 'PAYTM')], default='COD', max_length=30)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Menu_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_category', models.CharField(max_length=100)),
                ('item_description', models.TextField(default='')),
                ('item_cost', models.PositiveIntegerField()),
                ('veg_nonVeg', models.CharField(choices=[('Veg', 'Veg'), ('Non Veg', 'Non Veg')], max_length=100, null=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SNUmato.Restaurant')),
            ],
            options={
                'db_table': 'Menu_Item',
            },
        ),
        migrations.CreateModel(
            name='Current_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_cost', models.CharField(max_length=100)),
                ('item_quantity', models.PositiveIntegerField()),
                ('item_name', models.CharField(max_length=100)),
                ('item_id', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Current_order',
            },
        ),
    ]
