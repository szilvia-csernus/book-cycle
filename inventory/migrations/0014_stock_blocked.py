# Generated by Django 3.2.20 on 2023-09-12 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20230910_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='blocked',
            field=models.IntegerField(default=0),
        ),
    ]
