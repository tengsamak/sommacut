# Generated by Django 3.1.3 on 2021-03-23 05:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210226_1706'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=5)),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=20)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preaparing', 'Preaparing'), ('OnShipping', 'Onshipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('adminnote', models.CharField(blank=True, max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Canceled', 'Canceled')], default='New', max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
