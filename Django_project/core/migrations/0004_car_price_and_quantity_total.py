# Generated by Django 5.0.1 on 2024-03-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contactusmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price_and_quantity_total',
            field=models.IntegerField(default=0),
        ),
    ]