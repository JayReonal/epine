# Generated by Django 4.2.4 on 2023-10-07 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0007_yield_calculated_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pinevalue',
            name='name',
        ),
        migrations.AddField(
            model_name='pinevalue',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pine.category'),
        ),
    ]
