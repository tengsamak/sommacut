# Generated by Django 3.1.3 on 2022-05-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='usertype',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Re-Seller', 'Re-Seller'), ('VENDOR', 'VENDOR')], default='Normal', max_length=20),
        ),
    ]
