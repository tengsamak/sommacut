# Generated by Django 3.2.2 on 2024-08-02 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0012_auto_20240802_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('New', 'New'), ('Inactive', 'Inactive'), ('True', 'True'), ('False', 'False')], default='True', max_length=10),
        ),
    ]
