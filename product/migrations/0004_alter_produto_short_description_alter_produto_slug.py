# Generated by Django 4.1.7 on 2023-03-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_variacao_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='short_description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Descrição curta'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug'),
        ),
    ]
