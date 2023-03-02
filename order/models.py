from django.db import models
from django.contrib.auth.models import User
"""
Pedido:
        user - FK User
        total - Float
        status - Choices
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),

        ItemPedido:
            pedido - FK pedido
            produto - Char
            produto_id - Int
            variacao - Char
            variacao_id - Int
            preco - Float
            preco_promocional - Float
            quantidade - Int
            imagem - Char
"""
STATUS_CHOICES = (
    ('A', 'Aprovado'), ('P', 'Pendente'), ('C', 'Criado'), 
    ('R', 'Recusado'), ('E', 'Enviado'), ('F', 'Finalizado'),
)


class Pedido(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, verbose_name='Usuário')
    total = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C')
    
    def __str__(self):
        return f'Pedido Nº {self.pk}'


class ItemPedido(models.Model):
    order = models.ForeignKey(Pedido, models.CASCADE, verbose_name='Pedido')
    product = models.CharField('Produto', max_length=255)
    product_id = models.PositiveIntegerField('ID do produto')
    variation = models.CharField('Variação', max_length=100)
    variation_id = models.PositiveIntegerField('ID da variação')
    price = models.FloatField(verbose_name='Preço')
    promotional_price = models.FloatField('Preço promocional')
    quantity = models.PositiveIntegerField('Quantidade')
    image = models.CharField(max_length=2000, verbose_name='Imagem')

    def __str__(self):
        return f'Item do {self.order}'.capitalize()
    
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'
