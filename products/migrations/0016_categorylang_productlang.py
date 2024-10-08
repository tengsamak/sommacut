# Generated by Django 3.1.3 on 2021-05-25 05:30

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('EN', 'English'), ('KH', 'Khmer'), ('CN', 'Chinese')], max_length=6)),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('detail', ckeditor_uploader.fields.RichTextUploadingField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('EN', 'English'), ('KH', 'Khmer'), ('CN', 'Chinese')], max_length=6)),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorylangs', to='products.category')),
            ],
        ),
    ]
