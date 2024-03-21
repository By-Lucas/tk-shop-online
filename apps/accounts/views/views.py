from typing import Any

from django.urls import reverse_lazy
from django.contrib import messages, auth
from django.http import HttpResponse, JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login

from accounts.models import User
from company.models.models_company import Company
#from helpers.decorators import admin_level_required
from accounts.forms import UserForm, UserUpdateForm
#from company.form import CollaboratorForm, CompanyForm
#from helpers.commons import LEGAL_PERSON, NATURAL_PERSON
#from company.models.models_collaborator import Collaborator
from helpers.utils import get_unique_username, send_notification, send_verification_email


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'Você já está logado!')
        return redirect('home:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {email}!')
            return redirect('home:home')
        else:
            messages.error(request, 'Credenciais de login inválidas.')
            return redirect('home:home')


def logout_user(request):
    auth.logout(request)
    messages.info(request, 'Logout feito.')
    return redirect('home:home')


def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
    
        if user_form.is_valid():
            user = user_form.save(commit=False)
            password =request.POST.get('password1')
            user.password1 = password
            user.password2 = password
            user.username = get_unique_username(user.email)
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('home:home')
        else:
            messages.error(request, f'Por favor, corrija os erros abaixo. {user_form.errors}')

    else:
        user_form = UserCreationForm()
        
    return redirect('home:home')


class UpdateCollaborador(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update-profile.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        collaborator = get_object_or_404(Collaborator, user=user)
        
        user_form = UserUpdateForm(instance=user)
        collaborator_form = CollaboratorForm(instance=collaborator.user, user=request.user)
        
        context = {
            'pk':pk,
            'user_form': user_form,
            'collaborator_form': collaborator_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        collaborator = get_object_or_404(Collaborator, user=user)
        user_form = UserUpdateForm(self.request.POST, instance=user)
        collaborator_form = CollaboratorForm(self.request.POST, self.request.FILES, instance=collaborator, user=request.user)
        
        if user_form.is_valid() and collaborator_form.is_valid():
            form_u = user_form.save(commit=False)
            form_u.save()
            form_c = collaborator_form.save(commit=False)
            form_c.user_id = user
            form_c.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            
            return redirect('company:list_collaborators')
        else:
            messages.error(request, f'Obteve o seguinte erro {user_form.errors.as_text()} {collaborator_form.errors.as_text()}')

        context = {
            'pk':pk,
            'user_form': user_form,
            'collaborator_form': collaborator_form,
        }
        return self.render_to_response(context)


class UpdateProfileCompany(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('user_profile')
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {}
        profile_user = self.request.user
        collaborator = Collaborator.objects.get(user=profile_user)
        
        user_form = UserUpdateForm(instance=profile_user)
        collaborator_form = CollaboratorForm(instance=collaborator, user=profile_user)
        form_password = PasswordChangeForm(user=profile_user)
        
        if profile_user.is_superuser or profile_user.user_charisma or collaborator.is_active and collaborator.permission == "super_admin":
            context['company']=collaborator.company
            context['company_form'] = CompanyForm(instance=collaborator.company)
        
        context['user_form'] = user_form
        context['profile_user'] = profile_user
        context['collaborator'] = collaborator
        context['form_password'] = form_password
        context['collaborator_form'] = collaborator_form
        return render(request, self.template_name, context)
    
    def post(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {}
        profile_user = self.request.user
        collaborator = Collaborator.objects.get(user=profile_user)
        
        if self.request.GET.get('profile'):
            user_form = UserUpdateForm(self.request.POST, self.request.FILES, instance=profile_user)
            collaborator_form = CollaboratorForm(self.request.POST, self.request.FILES, instance=collaborator, user=request.user)
            context['user_form'] = user_form
            context['profile_user'] = profile_user
            context['collaborator_form'] = collaborator_form
            
            if user_form.is_valid() and collaborator_form.is_valid():
                user_form.save()
                collaborator_form.save()
                
                messages.success(request, 'Perfil editado com sucesso!')
                return redirect('accounts:profile')
        
        if self.request.GET.get('company'):
            company_form = CompanyForm(request.POST, request.FILES, instance=collaborator.company)
            context['company_form'] = company_form
            
            if company_form.is_valid():
                company_form.save()
                
                messages.success(request, 'Empresa editada com sucesso.')
                return redirect('accounts:profile')
        
        return self.render_to_response(context)


           
@login_required
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        message = ''
        new_password = request.POST.get('new_password1')

        if request.POST.get('old_password') == "" or new_password == "" or request.POST.get('new_password2') == "":
            message = 'Todos os campos deve estar preenchidos corretamente'
            return JsonResponse({'message': message, 'status': False})
        if len(new_password) < 8:
            message = 'A nova senha deve ter pelo menos 8 caracteres.'
            return JsonResponse({'message': message, 'status': False})
        elif not any(char.isdigit() for char in new_password):
            message = 'A nova senha deve conter pelo menos um número.'
            return JsonResponse({'message': message, 'status': False})
        elif not any(char.isupper() for char in new_password):
            message = 'A nova senha deve conter pelo menos uma letra maiúscula.'
            return JsonResponse({'message': message, 'status': False})

        if form.is_valid():
            form.save()
            message = 'Senha alterada com sucesso, da proxima vez faça o login com a nova senha.'
            update_session_auth_hash(request, form.user)
            return JsonResponse({'message': message, 'status': True})
        else:
            message = f'Por favor corrija os erros abaixo: {form.errors.as_text().split("* ")[2]}.'
            return JsonResponse({'message': message, 'status': False})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email__exact=email).first()

            # send reset password email
            mail_subject = 'Redefina sua senha'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'O link de redefinição de senha foi enviado para o seu endereço de e-mail.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Conta não existe')
            return redirect('accounts:forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Redefina sua senha')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'Link de recuperação de senha expirado!')
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Redefinição de senha bem-sucedida')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Senha não confere!')
            return redirect('accounts:reset_password')
    return render(request, 'accounts/reset_password.html')

    
# FUNCIONALIDADES QUE SERÃO UTILIZADAS NO FUTURO =====================================

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Parabéns! Sua conta está ativada.')
        return redirect('home')
    else:
        messages.error(request, 'Link de ativação inválido')
        return redirect('home')
    
    
def verify_view(request):
    """ Este código envia um sms para o contato do usuário"""
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username}: {user.code}"
        if not request.POST:
            # send sms
            print(code_user)
            #send_sms(code_user, user.phone)
        if form.is_valid():
            num = form.cleaned_data.get('code')
            if str(code) == num:
                code.save()
                auth.login(request, user)
                messages.success(request, f'Seja bem vindo {user}')
                return redirect('home')
            else:
                messages.error(request, 'O código informado está incorreto, tente novamente.')
                return redirect('accounts:verify_view')
    return render(request, 'accounts/verify_code.html', {'form':form})

         
# REMOVER ESTE
@login_required
#@admin_level_required
def users(request):
    admin_clinic = UserClinic.objects.filter(user=request.user)

    clinic_ids = []
    for x in admin_clinic:
        clinic_ids.append(x.clinic.id)

    if request.user.user_clipse or request.user.is_superuser:
        users = UserClinic.objects.all().exclude(id=request.user.id).order_by('-id')
    else:
        users = UserClinic.objects.filter(clinic__in=clinic_ids).exclude(user=request.user.id).order_by('-id')
        print(users)

    return render(request, 'accounts/users.html', locals())


@login_required
#@admin_level_required
def users_list(request):
    is_active_users = True
    is_active_clinic = True

    admin_clinic = UserClinic.objects.filter(user=request.user)

    clinic_ids = []
    for x in admin_clinic:
        clinic_ids.append(x.clinic.id)

    if request.user.user_clipse or request.user.is_superuser:
        users = UserClinic.objects.all().exclude(id=request.user.id).order_by('-id')
    else:
        users = UserClinic.objects.filter(clinic__in=clinic_ids).exclude(user=request.user.id).order_by('-id')

    return render(request, 'accounts/users_list.html', locals())


@login_required
#@admin_level_required
def edit_user(request, pk):
    profile = get_object_or_404(User, id=pk)

    try:
        clinic = UserClinic.objects.get(user=profile)
    except UserClinic.DoesNotExist:
        clinic = None

    title_page = 'Editar Usuário'

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        permission_form = UserClinicPermissionForm(data=request.POST, instance=clinic, user=request.user)

        if form.is_valid() and permission_form.is_valid():
            person_type = form.cleaned_data['cnpj_cpf']

            user = form.save(commit=False)
            user.username = get_unique_username(user.email)
            user.set_password(user.password)

            if len(person_type) > 14:
                user.person_type = LEGAL_PERSON
            else:
                user.person_type = NATURAL_PERSON

            user.save()

            if permission_form.cleaned_data['clinic'] is None:
                pform = permission_form.save(commit=False)
            else:
                pform = permission_form.save(commit=False)
                pform.user = user
                pform.save()

            messages.success(request, 'Usuário editado com sucesso.')
            return redirect('accounts:users')

    else:
        form = UserProfileForm(instance=profile, user=request.user)
        permission_form = UserClinicPermissionForm(instance=clinic, user=request.user)

    is_active_clinic = True
    is_active_users = True

    return render(request, 'accounts/add_user.html', locals())
