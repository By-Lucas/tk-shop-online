from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


from accounts.models import User
#from products.models  import Product
#from core.models import ConfigModel, TelegramMyGroup


#config = ConfigModel.objects.all().first()
#chat_ids = TelegramMyGroup.objects.all().values_list('chat_id', flat=True)


#@receiver(post_save, sender=Product)
def post_save_create_product_receiver(sender, instance, created, **kwargs):
    if created:
        if config.send_product_group:
            print(instance.image.url)
            print(chat_ids)
            print('ENVIANDO')

#@receiver(pre_save, sender=Product)
def pre_save_product_receiver(sender, instance, **kwargs):
    if instance.pk is None:
        if config.send_product_group:
            print(chat_ids)
            print('PREPARANDO PARA ENVIAR')
        
        
@receiver(post_save, sender=User)
def post_save_create_collaborator_receiver(sender, instance, created, **kwargs):
    if created:
        print('Signal: Creating collaborator')
        #collaborator = Collaborator.objects.create(user=instance)
        #print('Collaborator created:', collaborator)
    else:
        print('Signal: Updating collaborator')
        # try:
        #     #collaborator = Collaborator.objects.get(user=instance)
        #     # Realize as atualizações necessárias no objeto colaborador
        #     collaborator.save()
        #     print('Collaborator updated:', collaborator)
        # except Collaborator.DoesNotExist:
        #     print('Collaborator does not exist. Creating...')
        #     collaborator = Collaborator.objects.create(user=instance)
        #     print('Collaborator created:', collaborator)