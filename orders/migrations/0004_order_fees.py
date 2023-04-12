# Generated by Django 3.0.8 on 2020-08-22 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_shippingcosts'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fees',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
