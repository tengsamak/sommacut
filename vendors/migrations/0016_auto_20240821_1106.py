# Generated by Django 3.2.2 on 2024-08-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0015_vendor_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment_v',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment_v',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
