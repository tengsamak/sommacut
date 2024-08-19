# Generated by Django 3.1.3 on 2023-06-22 02:33
# field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20230604_1654'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wishlist', '0004_wish_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wish_list',
            options={'ordering': ['-created_at'], 'verbose_name': 'Wish_list', 'verbose_name_plural': 'Wish_lists'},
        ),
        migrations.AddField(
            model_name='wish_list',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wish_list',
            name='variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='wishl_ist', to='products.variants'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wish_list',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to='products.product'),
        ),
        migrations.AlterField(
            model_name='wish_list',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
