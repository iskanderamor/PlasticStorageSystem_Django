# Generated by Django 4.0.3 on 2022-10-17 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0017_customuser_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
