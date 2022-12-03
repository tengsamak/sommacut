# Generated by Django 3.1.3 on 2022-05-11 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_auto_20210506_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='companyname',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='contactname',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('New', 'New'), ('False', 'False'), ('Approved', 'Approved')], default='New', max_length=10),
        ),
    ]
