# Generated by Django 4.0.3 on 2022-10-02 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0008_expenses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenses',
            old_name='employee_id',
            new_name='employee',
        ),
    ]
