# Generated by Django 4.2.4 on 2024-02-28 16:40

from django.db import migrations, models
import django.db.models.deletion
import helpers.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('offer_group', models.URLField(blank=True, max_length=2500, null=True, verbose_name='Grupo de ofertas principal')),
                ('time_hours_product', models.IntegerField(default=72, verbose_name='Tempo para deletar cada produto')),
                ('image', models.FileField(blank=True, null=True, upload_to=helpers.utils.image_company_path, verbose_name='Logo')),
                ('image_aba', models.FileField(blank=True, null=True, upload_to=helpers.utils.image_company_path, verbose_name='Imagem da aba')),
                ('send_product_group', models.BooleanField(blank=True, default=False, help_text='Ao salvar deseja enviar os produtos para os grupos do whtsapp e telegram?', null=True, verbose_name='Enviar produto para os grupos?')),
                ('send_product_description', models.TextField(blank=True, default='✅{titulo}✅\n                                               \n\n🔥 R${preco}\n                                               \n🔖 Use o cupom: {cupom}\n                                               \n\n🛍 Compre aqui: {link_produto}\n                                               \n😄 Convide seus amigos e familiares para participarem dos nossos grupos de promoção: {link_do_grupo}\n                                               \n⚠O link da foto na promo, Não está Clicável ? É só adicionar um dos ADMS em\xa0seus\xa0contatos', help_text='Alem das informações princioais, digite aqui outra informação que deseja enviar: Use o modelo descrito como base', null=True, verbose_name='Descrição para envio da mensagem')),
            ],
            options={
                'verbose_name': 'Configurações da empresa',
                'verbose_name_plural': 'Configurações das empresas',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Nome da rede social')),
                ('image', models.FileField(blank=True, help_text='Imagem exibição das redes sociais.', null=True, upload_to=helpers.utils.image_company_path, verbose_name='Imagem')),
                ('url_image', models.ImageField(blank=True, help_text='Caso nao queira fazer upload de da imagem, cole a URL da imagem aqui', max_length=2000, null=True, upload_to='', verbose_name='URL da imagem/video')),
                ('url_social', models.URLField(blank=True, max_length=2000, null=True, verbose_name='URL da rede social')),
            ],
            options={
                'verbose_name': 'Redes sociais',
                'verbose_name_plural': 'Redes sociais',
            },
        ),
        migrations.CreateModel(
            name='WhtasappGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do grupo do whatsapp')),
                ('group_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID do grupo do whatsapp')),
                ('send_msg', models.BooleanField(default=True, verbose_name='Enviar menssávem para o grupo?')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Grupo whatsapp',
                'verbose_name_plural': 'Grupo whatsapp',
            },
        ),
        migrations.CreateModel(
            name='TelegramGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do grupo telegram')),
                ('group_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='ID do grupo telegram')),
                ('send_msg', models.BooleanField(default=True, verbose_name='Enviar menssávem para o grupo?')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Grupo telegram',
                'verbose_name_plural': 'Grupo telegram',
            },
        ),
        migrations.CreateModel(
            name='AuthWhatsappModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('token', models.CharField(blank=True, help_text='Token liberado pela plataforma ultramsg', max_length=200, null=True, verbose_name='Token')),
                ('insitance_id', models.CharField(blank=True, help_text='Insistance ID liberado pela plataforma ultramsg', max_length=200, null=True, verbose_name='Insistance ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Autenticação Whatsapp',
                'verbose_name_plural': 'Autenticação Whatsapp',
            },
        ),
        migrations.CreateModel(
            name='AuthTelegramModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('bot_name', models.CharField(blank=True, help_text='Nome do bot Telegram', max_length=100, null=True, verbose_name='Nome do Bot')),
                ('bot_token', models.CharField(blank=True, help_text='Token do bot Telegram', max_length=500, null=True, verbose_name='Token')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Autenticação Telegram',
                'verbose_name_plural': 'Autenticação Telegram',
            },
        ),
    ]
