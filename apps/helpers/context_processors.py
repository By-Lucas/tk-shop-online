# from clinic.models.model_clinic import Clinic
# from accounts.others_models.model_profile import UserProfile


def get_clinic(request):
    try:
        clinic = Clinic.objects.get(user=request.user)
    except:
        clinic = None
    return dict(clinic=clinic)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


def get_clipse_permission(request):
    if request.user.is_authenticated and request.user.user_clipse or request.user.is_superuser:
        user_clipse = True
    else:
        user_clipse = False

    return {'user_clipse': user_clipse}


def get_clinic_administrator(request):
    if request.user.is_authenticated and request.user.permission == 'adm_access':
        user_admin_clinic = True
    else:
        user_admin_clinic = False

    return {'user_admin_clinic': user_admin_clinic}


def get_commom_user(request):
    if request.user.is_authenticated and request.user.user_commom_access == 'adm_access':
        commom_user = True
    else:
        commom_user = False

    return {'commom_user': commom_user}
