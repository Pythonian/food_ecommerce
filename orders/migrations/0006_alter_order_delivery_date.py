# Generated by Django 4.2.4 on 2023-08-15 03:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 19, 3, 34, 9, 701617)),
        ),
    ]
