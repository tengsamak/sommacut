# Generated by Django 3.2.2 on 2024-08-11 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20240811_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_timer',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
