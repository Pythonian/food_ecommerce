# Generated by Django 4.2.4 on 2023-08-15 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='state',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='cac_file',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='government_id',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='state',
        ),
    ]
