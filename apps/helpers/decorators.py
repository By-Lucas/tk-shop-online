from functools import wraps
from django.http import HttpResponseBadRequest, HttpResponseForbidden

from helpers import commons
from company.models.models_company import UserCompanyRole


def company_user_has_permission(required_permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if request.user.is_authenticated:
            
                # Verifica se a conta do usuário está ativa.
                if not user.is_active:
                    return HttpResponseForbidden("Sua conta está desativada.")
                
                if user.is_superuser or user.user_charisma or user.is_admin:
                    return view_func(request, *args, **kwargs)
                
                # Tenta acessar o UserCompanyRole de forma segura.
                user_company_role = getattr(user, 'usercompanyrole', None)
                
                # Se o UserCompanyRole não existir ou o nível de acesso não estiver na lista de permissões requeridas, retorna proibido.
                if not user_company_role or user_company_role.access_level not in required_permission:
                    return HttpResponseBadRequest("Você não tem permissão para acessar esta página.")
            else:
                return HttpResponseForbidden("Faça login para ter acesso aos dados.")
        
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def company_status_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            company_status = UserCompanyRole.objects.filter(user=request.user).first()

            if not request.user.is_active:
                return HttpResponseForbidden("Sua conta de usuário está desativada.")
            
            if request.user.is_superuser and request.user.user_charisma and request.user.is_admin:
                return view_func(request, *args, **kwargs)
            
            if not company_status:
                return HttpResponseForbidden("Usuário não associado a nenhuma empresa.")
            
            if company_status.role == commons.BLOCKED:
                return HttpResponseBadRequest("A empresa está bloqueada, por favor fale com administrador Charisma.")
            
            if company_status.role == commons.SUSPENDED:
                return HttpResponseForbidden("A empresa está suspensa, por favor fale com administrador Charisma.")
        else:
            return HttpResponseForbidden("Faça login para ter acesso aos dados.")
    
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def charisma_level_required(view_func):
    def _decorator(request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            if not request.user.is_active:
                return HttpResponseForbidden("Sua conta está desativada.")
            
            elif request.user.is_superuser and request.user.user_charisma and request.user.is_admin:
                response = view_func(request, *args, **kwargs)
                return response
            
            else:
                return HttpResponseBadRequest("Você não tem permissão para acessar esta página.")
        else:
            return HttpResponseForbidden("Faça login para ter acesso aos dados.")
    
    return wraps(view_func)(_decorator)
