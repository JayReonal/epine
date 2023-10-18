# Generated by Django 4.2.4 on 2023-10-08 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0009_rename_cost_stock_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='stock',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
