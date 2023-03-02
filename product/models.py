from django.db import models
from PIL import Image
from django.utils.text import slugify
from utils import functions

CHOICES = ('V', 'Variável'), ('S', 'Simples')
IMG_DEFAULT_SIZE = (400, 250)


class Produto(models.Model):
    name = models.CharField('Nome', max_length=255)
    short_description = models.TextField(
        'Descrição curta', blank=True, null=True, max_length=200
    )
    long_description = models.TextField('Descrição longa', blank=True, null=True)
    image = models.ImageField('Imagem do produto', upload_to='products/img/%Y/%b/')
    slug = models.SlugField('Slug', unique=True, blank=True, null=True)
    marketing_price = models.FloatField('Preço marketing')
    promotional_marketing_price = models.FloatField(
        'Preço marketing promocional', default=0
    )
    variation_type = models.CharField(
        'Tipo', max_length=1, choices=CHOICES, default='V'
    )
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            pk = Produto.objects.all().order_by('-id').first().id + 1
            self.slug = f'{slugify(self.name)}-{pk}'
            
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):        
        img = Image.open(self.image.path)
        x, y = img.size
        if x <= IMG_DEFAULT_SIZE[0] and y <= IMG_DEFAULT_SIZE[1]:
            img.close()
            return
        
        new_img = img.resize(IMG_DEFAULT_SIZE, Image.ANTIALIAS)
        new_img.save(self.image.path, quality=70, optimize=True)
        img.close()
        new_img.close()
    
    def get_marketing_price_formatted(self):
        return functions.format_money_value(self.marketing_price)
    get_marketing_price_formatted.short_description = 'Preço'
    
    def get_promotional_price_formatted(self):
        return functions.format_money_value(self.promotional_marketing_price)
    get_promotional_price_formatted.short_description = 'Preço promocional'

 
class Variacao(models.Model):
    product = models.ForeignKey(Produto, models.CASCADE, verbose_name='Produto')
    name = models.CharField('Nome', max_length=255)
    price = models.FloatField('Preço')
    promotional_price = models.FloatField('Preço promocional', default=0)
    stock = models.PositiveIntegerField('Estoque', default=1)
    
    def __str__(self):
        return self.name or self.product.name
    
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
