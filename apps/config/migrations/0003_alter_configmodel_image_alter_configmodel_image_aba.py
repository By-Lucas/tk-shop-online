# Generated by Django 4.2.4 on 2024-02-28 16:51

from django.db import migrations, models
import helpers.utils


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_alter_configmodel_image_alter_configmodel_image_aba_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configmodel',
            name='image',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to=helpers.utils.image_path, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='configmodel',
            name='image_aba',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to=helpers.utils.image_path, verbose_name='Imagem da aba'),
        ),
    ]
