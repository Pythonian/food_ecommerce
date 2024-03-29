# Generated by Django 4.2.4 on 2023-08-15 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='alt_text',
        ),
        migrations.RemoveField(
            model_name='product',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='product',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='product',
            name='units_sold',
        ),
        migrations.AddField(
            model_name='product',
            name='calories',
            field=models.CharField(default='', help_text='The amount of energy provided by the food.Example: 150 (kcal)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='carbohydrates',
            field=models.CharField(default='', help_text='The total amount of carbohydrates in the food, including sugars, fiber, and starches. Example: 20.3 (g)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='delivery_time',
            field=models.CharField(default='', help_text='Time it will take for this food to be delivered.', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='fats',
            field=models.CharField(default='', help_text='The total amount of fats in the food, including saturated fats and unsaturated fats. Example: 5.2 (g)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='fiber',
            field=models.CharField(default='', help_text='The amount of dietary fiber in the food. Example: 3.5 (g)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='minerals',
            field=models.CharField(default='', help_text='The amount of various minerals present in the food. Example: Iron: 2.3 mg, Calcium: 120 mg', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='protein',
            field=models.CharField(default='', help_text='The amount of protein in the food. Example: 8.5 (g)', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='vitamins',
            field=models.CharField(default='', help_text='The amount of various vitamins present in the food. Example: Vitamin C: 10 mg, Vitamin A: 200 IU', max_length=200),
            preserve_default=False,
        ),
    ]
