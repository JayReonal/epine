# Generated by Django 4.2.4 on 2023-10-17 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pine', '0019_badpine'),
    ]

    operations = [
        migrations.CreateModel(
            name='bad_pine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pine.category')),
            ],
        ),
    ]
