# Generated by Django 3.2.2 on 2024-07-31 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0006_remove_wish_list_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish_list',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
