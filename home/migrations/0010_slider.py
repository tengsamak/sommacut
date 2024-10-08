# Generated by Django 3.1.3 on 2024-01-30 10:42

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20231202_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='550', help_text='192x550', upload_to='uploads/slider', width_field='1920')),
                ('headerslide', models.CharField(help_text='ex:For Summer, for Holiday.. ', max_length=200)),
                ('titleslide', models.CharField(help_text='Your Main Popose for slid, ex:Discount 20%, Sale off, Free Delivery..', max_length=100)),
                ('descriptionslid', models.CharField(help_text='detail about your promotion slide', max_length=300)),
                ('linkslide', models.CharField(help_text='link to product or link to vendor product list', max_length=500)),
                ('startdate', models.DateField(help_text='Start date to post Slide image')),
                ('finishdate', models.DateField(help_text='Finish date for promotion')),
                ('statusslide', models.CharField(choices=[('Expired', 'Expired'), ('Valid', 'Valid'), ('Invalid', 'Invalid')], max_length=100)),
                ('supportedby', models.CharField(help_text='Vendor Name', max_length=500)),
                ('slideterm', ckeditor.fields.RichTextField(help_text='detail about contact vendor with developer on slide show, design and date post or expire')),
            ],
        ),
    ]
