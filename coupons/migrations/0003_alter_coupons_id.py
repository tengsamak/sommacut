# Generated by Django 3.2.2 on 2024-07-31 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_auto_20220430_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
