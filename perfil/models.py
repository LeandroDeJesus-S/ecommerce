from django.db import models
from django.contrib.auth.models import User
from utils.validacpf import valida_cpf
from django.core.validators import RegexValidator

STATE_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]
class Perfil(models.Model):
    user = models.OneToOneField(User, models.CASCADE, verbose_name='Usuário')
    birthday = models.DateField(verbose_name='Data de nascimento')
    cpf = models.CharField(
        max_length=11, validators=[valida_cpf], verbose_name='CPF'
    )
    address = models.CharField(max_length=100, verbose_name='Endereço')
    number = models.CharField(max_length=5, verbose_name='Número')
    complement = models.CharField(max_length=30, verbose_name='Complemento')
    neighborhood = models.CharField('Bairro', max_length=30)
    cep = models.CharField(
        'CEP', max_length=8, validators=[RegexValidator('^\d{8}$')]
    )
    city = models.CharField('Cidade', max_length=30)
    state = models.CharField(
        'Estado', max_length=2, default='AC', choices=STATE_CHOICES
    )

    def __str__(self) -> str:
        return self.user.username

    def clean(self) -> None:
        super().clean()
        
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
