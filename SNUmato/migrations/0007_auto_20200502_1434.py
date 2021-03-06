# Generated by Django 2.2.3 on 2020-05-02 09:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('SNUmato', '0006_auto_20200502_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.CharField(max_length=7),
        ),
    ]
