# Generated by Django 4.0.3 on 2022-11-10 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lsmsApp', '0038_rename_state_sales_ranking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='ranking',
            new_name='condition',
        ),
    ]