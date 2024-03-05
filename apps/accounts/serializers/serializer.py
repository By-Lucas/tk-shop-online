from datetime import datetime, timezone

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from company.models.models_company import UserCompanyRole, CompanyModels


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # Primeiro, chame a validação padrão para verificar as credenciais do usuário
        data = super().validate(attrs)
        user = self.user
        
        token = self.get_token(self.user)
        token['username'] = user.username
        token['name'] = user.name
        token['email'] = user.email
        exp = datetime.now(timezone.utc) + token.lifetime
        token['exp'] = exp.timestamp()

        if user.is_superuser or user.user_charisma or user.is_admin:
            data['token'] = str(token)
            return data
        
        if not user.is_active:
            msg = _("Usuário desativado")
            raise serializers.ValidationError(msg)
        
        if user.is_company:
            user_company_role = UserCompanyRole.objects.filter(user=user).first()
            if user_company_role:
                company = CompanyModels.objects.filter(api_key=user_company_role.company.api_key, secret_key=user_company_role.company.secret_key).first()
                # Verifica se a empresa está bloqueada ou suspensa
                if company.status in ['blocked', 'suspended']:
                    msg = _("A empresa está {}.").format(company.get_status_display().lower())
                    raise serializers.ValidationError(msg)
                
                # Adiciona campos personalizados ao token
                token['company'] = company.id
                token['role'] = user_company_role.role
                data['token'] = str(token)
                return data
        else:
            msg = _("Usuário não tem nenhuma empresa cadastrada")
            raise serializers.ValidationError(msg)

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

