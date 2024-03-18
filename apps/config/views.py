import json
import time
import requests
from loguru import logger

from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from company.models.models_company import Company
from config.models.models_whatsapp import AuthWhatsappModel, WhtasappGroups


def get_groups_whatsapp(request):
    settings = AuthWhatsappModel.objects.first()
    token__ = settings.token
    insistance__ = settings.insitance_id
    list_group = request.GET.get("list_whatsapp", False)
    
    groups_data = []
    my_groups = WhtasappGroups.objects.all()
    
    context = {
        'my_groups': my_groups,
        'groups_data': groups_data
        }
        
    if list_group: 
        try:
            url = f"https://api.ultramsg.com/{insistance__}/groups"
            querystring = {"token": token__}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.get(url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                for group in response.json():
                    if WhtasappGroups.objects.filter(group_id=group["id"]):
                        print("Continuando")
                        continue
                        
                    groups_data.append({"name": group["name"], "id": group["id"]})
                    context['groups_data'] = groups_data
                
                return JsonResponse({'groups_data':groups_data, 'message':'Grupos listados com sucesso.'})
        
        except requests.exceptions.ConnectionError:
            logger.error('Uma conexão estabelecida foi anulada pelo software no computador host')
            return JsonResponse({'status':False, 'message':'Uma conexão estabelecida foi anulada pelo software no computador host'})

        else:
            error_message = f'Ocorreu o seguinte erro ao enviar mensagem para o grupo do whatsapp: {response.text}'
            return JsonResponse({'groups_data':[], 'message':error_message})
        
    return render(request, 'config/grupos_whatsapp.html', context)


def get_my_groups_whatsapp(request):
    settings = AuthWhatsappModel.objects.first()
    
    groups_data = []
    for group in WhtasappGroups.objects.all():
        context = {
            'name': group.name,
            'pk': group.pk
            }
        groups_data.append(context)

    return JsonResponse({'my_groups': groups_data})
    
    
def save_selected_groups(request):
    selected_groups = request.POST.getlist("selected_groups[]", [])  # Lista de nomes dos grupos
    selected_groups_ids = request.POST.getlist("selected_groups_ids[]", [])  # Lista de IDs dos grupos
    my_groups = [groups for groups in WhtasappGroups.objects.all()]

    if selected_groups and selected_groups_ids:
        for name, group_id in zip(selected_groups, selected_groups_ids):
            try:
                # Atualizar ou criar o objeto WhatsappGroups
                update, created = WhtasappGroups.objects.update_or_create(
                    company=Company.objects.first(),
                    group_id=group_id,
                    defaults={
                        "name":name,
                        "send_msg": True
                    }
                )
            except UnicodeTranslateError as e:
                logger.error(f"Erro ao processar o grupo {name}: {e}")
                return JsonResponse({"message": f"Erro ao processar o grupo {name}: {e}"})
        
    return JsonResponse({"my_groups": my_groups, "message": "Grupos salvos com sucesso."})


def delete_group(request, pk):
    group = get_object_or_404(WhtasappGroups, pk=pk)
    if group:
        group.delete()
        return JsonResponse({"message": "Grupo deletado com sucesso."})
    return JsonResponse({"message": "Erro ao deletar groupo."})
    
        