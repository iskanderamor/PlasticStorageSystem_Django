# Generated by Django 4.0.3 on 2022-10-26 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0019_invoiceproducts_employee_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
