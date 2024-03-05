import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.models import User
from company.models.models_company import UserCompanyRole


# Dados para conexão com aws
user = 'AKIA3AGL3QGUWCZHGSUG'
pw   = 'BKQh8KM6Nm7gmxvGJ0pMFXKHuV8rcPZXCvUPbh/pGdxD'
host = 'email-smtp.us-east-1.amazonaws.com'
port = 465
me   = 'news@charismabi.com'
you  = 'it@charismabi.com'


class ResetPasswordView(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        from_email = settings.DEFAULT_FROM_EMAIL
        
        if not User.objects.filter(email=email).exists():
            return Response({'error': 'Não existe um usuário com este endereço de e-mail.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email__exact=email)
        
        context = {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }
        
        try:
            company = UserCompanyRole.objects.get(user=user)
            if company:
                context['domain'] = company.company.url_company
        except (TypeError, ValueError, OverflowError, UserCompanyRole.DoesNotExist) as e:
            pass
        
        # send reset password email
        mail_subject = 'Redefina sua senha'
        email_template_name = 'accounts/emails/reset_password_email.html'
        email_body = render_to_string(email_template_name, context)
        
        # Localhost
        mail = EmailMessage(mail_subject, email_body, from_email, to=[email])
        mail.content_subtype = "html"
        mail.send()
            
        # Conexão aws - im review
        # msg = MIMEMultipart('alternative')
        # msg['From'] = me
        # msg['Subject'] = mail_subject
        # msg['To'] = email
        # part = MIMEText(email_body, 'html')
        # msg.attach(part)
        
        # # Establish an SMTP connection with AWS SES
        # s = smtplib.SMTP_SSL(host, port)
        # s.login(user, pw)
        
        # try:
        #     # Send the email
        #     s.sendmail(me, [email], msg.as_string())
        # except smtplib.SMTPException as e:
        #    print(f"An error occurred while sending the email: {e}")
        # finally:
        #     s.quit()
        return Response({'message': 'O link de redefinição de senha foi enviado para o seu endereço de e-mail.'}, status=status.HTTP_200_OK)


class ResetPasswordConfirmView(APIView):

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Verifica se o token é válido
        if user is not None and default_token_generator.check_token(user, token):
            # Define a nova senha
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Senha redefinida com sucesso.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)
