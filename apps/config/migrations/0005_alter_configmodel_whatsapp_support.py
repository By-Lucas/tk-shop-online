# Generated by Django 4.2.4 on 2024-03-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_remove_configmodel_offer_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configmodel',
            name='whatsapp_support',
            field=models.CharField(blank=True, max_length=18, null=True, verbose_name='Contato Whatsapp para Suporte'),
        ),
    ]
