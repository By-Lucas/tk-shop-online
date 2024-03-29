# Generated by Django 4.2.4 on 2024-03-01 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_slug_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug_product',
            field=models.SlugField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]
