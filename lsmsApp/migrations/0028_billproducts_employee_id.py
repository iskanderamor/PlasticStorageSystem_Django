# Generated by Django 4.0.3 on 2022-10-30 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0027_remove_employee_bill_bill_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='billproducts',
            name='employee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lsmsApp.employee'),
        ),
    ]