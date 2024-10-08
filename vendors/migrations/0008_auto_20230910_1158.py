# Generated by Django 3.1.3 on 2023-09-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0007_auto_20230722_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='APM',
            field=models.TextField(help_text='Accepted Payment Method', null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='facebook',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='ig',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='tiktok',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='www',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='companydetail',
            field=models.TextField(help_text='Comapy Vision Mission and type of business', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='companyname',
            field=models.CharField(help_text='Company Name', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('New', 'New'), ('Inactive', 'Inactive')], default='New', max_length=10),
        ),
    ]
