# Generated by Django 4.0.3 on 2022-10-12 11:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0014_alter_purchaseproducts_product_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceproducts',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
