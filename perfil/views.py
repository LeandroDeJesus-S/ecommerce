from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from . import models, forms
import copy


class BasePerfil(View):
    template_name = 'create.html'
    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        
        self.perfil = None
        if self.request.user.is_authenticated:  # updating data
            self.perfil = models.Perfil.objects.filter(user=self.request.user).first()
            self.context = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user
                ),
                'perfil_form': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                ),
            }
            
        else:  # registering new users
            self.context = {
                'user_form': forms.UserForm(data=self.request.POST or None),
                'perfil_form': forms.PerfilForm(data=self.request.POST or None),
            }
            
        if self.request.user.is_authenticated:
            self.template_name = 'update.html'
            
        self.rendering = render(self.request, self.template_name, self.context)
        
        self.userform = self.context['user_form']
        self.perfilform = self.context['perfil_form']
    
    def get(self, *args, **kwargs):
        return self.rendering


class CreatePerfil(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(self.request, 'Formulário invalido.')
            return self.rendering
        
        userform_data = self.userform.cleaned_data
        USERNAME = userform_data.get('username')
        PASSWORD = userform_data.get('password')
        EMAIL = userform_data.get('email')
        FIRST_NAME = userform_data.get('first_name')
        LAST_NAME = userform_data.get('last_name')
        
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        if self.request.user.is_authenticated:  # update
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = USERNAME
            if PASSWORD:
                user.set_password(PASSWORD)
            user.email = EMAIL
            user.first_name = FIRST_NAME
            user.last_name = LAST_NAME
            user.save()
            
            if not self.perfil:
                perfil = models.Perfil(user=user, **self.userform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.user = user
                perfil.save()
            
            messages.success(self.request, 'Dados atualizados com sucesso.')
            
        else:  # cadaster
            user = self.userform.save(commit=False)
            user.set_password(PASSWORD)
            user.save()

            perfil = self.perfilform.save(commit=False)
            perfil.user = user
            perfil.save()
            messages.success(self.request, 'Cadastro realizado com sucesso.')
        
        if PASSWORD: 
            auth = authenticate(
                self.request, username=USERNAME, password=PASSWORD
            )
            if auth:
                login(self.request, user)
                
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        if self.request.session.get('carrinho'):
            return redirect('product:purchase_summary')
        return redirect('perfil:create')


class UpdatePerfil(View):
    def get(self, *args, **kwargs):
        return HttpResponse('UpdatePerfil')


class LoginPerfil(UpdatePerfil):
    def post(self, *args, **kwargs):
        USERNAME = self.request.POST.get('username')
        PASSWORD = self.request.POST.get('password')
        user = authenticate(self.request, username=USERNAME, password=PASSWORD)
        if not USERNAME or not PASSWORD:
            messages.error(self.request, 'Preencha todos os campos.')
        
        elif user is None:
            messages.error(self.request, 'Usuário os senha incorretos.')
            
        else:
            login(self.request, user)
            messages.success(self.request, f'Você entrou como {user.get_username()}')
            return redirect('/')
            
        return redirect('perfil:create')


class LogoutPerfil(LoginPerfil):
    def get(self, *args, **kwargs):
        carrinho =  copy.deepcopy(self.request.session.get('carrinho', {}))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('/')
