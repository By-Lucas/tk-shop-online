# Generated by Django 4.2.4 on 2024-03-21 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_favoriteproductlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteproductlink',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='products.product'),
        ),
    ]