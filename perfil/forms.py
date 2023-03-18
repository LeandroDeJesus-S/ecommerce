from django import forms
from django.contrib.auth.models import User
from . import models
from django.core.exceptions import ValidationError


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        exclude = 'user',
        
    def clean(self, *args, **kwargs) -> None:
        super().clean(*args, **kwargs)
        cep = self.data.get('cep')
            
        sequence = cep[0] * len(cep)
        if cep == sequence:
            raise ValidationError({'cep':'Formulário inválido.'})
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(), label="Senha"
    )
    pass_confirmation = forms.CharField(
        required=False, widget=forms.PasswordInput(), label="Confirmação de senha"
    )
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'password', 'pass_confirmation', 
        )
    
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        USERNAME_ERROR_MESSAGE = 'Este nome de usuário já existe.'
        EMAIL_EXISTS_ERROR_MESSAGE = 'Este email já existe.'
        PASS_MATCH_ERROR_MESSAGE = 'As senhas não são iguais.'
        PASS_LEN_ERROR_MESSAGE = 'A senha precisa ter no mínimo 6 caracteres.'
        REQUIRED_FIELD_ERROR_MESSAGE = 'Este campo é obrigatório.'
        
        clean_data = self.cleaned_data
        error_messages = {}
        
        first_name = clean_data.get('first_name')
        last_name = clean_data.get('last_name')
        username = clean_data.get('user')
        email = clean_data.get('email')
        password = clean_data.get('password')
        pass_confirmation = clean_data.get('pass_confirmation')
        
        users = User.objects
        user_exists = users.filter(username=username).exists()
        email_exists = users.filter(email=email).exists()
        
        
        if self.user:
            if not first_name:
                error_messages['first_name'] = REQUIRED_FIELD_ERROR_MESSAGE
        
            if not last_name:
                error_messages['last_name'] = REQUIRED_FIELD_ERROR_MESSAGE
                
            if username != self.user and user_exists:
                error_messages['username'] = USERNAME_ERROR_MESSAGE
                
            if email != users.get(username=self.user).email and email_exists:
                error_messages['email'] = EMAIL_EXISTS_ERROR_MESSAGE
            
            if password and len(password) < 6:
                error_messages['password'] = PASS_LEN_ERROR_MESSAGE
                
            if password and password != pass_confirmation:
                error_messages['pass_confirmation'] = PASS_MATCH_ERROR_MESSAGE
        
        # new users
        else:
            if not first_name:
                error_messages['first_name'] = REQUIRED_FIELD_ERROR_MESSAGE
        
            if not last_name:
                error_messages['last_name'] = REQUIRED_FIELD_ERROR_MESSAGE
            
            if user_exists:
                error_messages['username'] = USERNAME_ERROR_MESSAGE
            
            if email_exists:
                error_messages['email'] = EMAIL_EXISTS_ERROR_MESSAGE
            
            if not password or not pass_confirmation:
                error_messages['password'] = REQUIRED_FIELD_ERROR_MESSAGE
                error_messages['pass_confirmation'] = REQUIRED_FIELD_ERROR_MESSAGE
                
            elif len(password) < 6:
                error_messages['password'] = PASS_LEN_ERROR_MESSAGE
            
            elif password != pass_confirmation:
                error_messages['pass_confirmation'] = PASS_MATCH_ERROR_MESSAGE


        if error_messages:
            raise forms.ValidationError(error_messages)