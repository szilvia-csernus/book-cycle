# Generated by Django 3.2.20 on 2023-09-27 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_stock_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(max_length=254, unique=True),
        ),
    ]