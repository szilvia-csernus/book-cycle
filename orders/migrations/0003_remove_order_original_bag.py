# Generated by Django 3.2.20 on 2023-09-22 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20230922_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='original_bag',
        ),
    ]
