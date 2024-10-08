# Generated by Django 3.2.2 on 2024-07-31 09:52
# field=models.ForeignKey(blank=True, default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor'),
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0010_alter_vendor_id'),
        ('products', '0020_auto_20240426_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='vendor',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='m_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Market Price or Original price', max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Sale price', max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='pro_code',
            field=models.CharField(blank=True, help_text='Product Code auto generated', max_length=5),
        ),
    ]
