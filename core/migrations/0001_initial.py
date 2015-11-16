# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtribuicaoCargo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('data_inicio', models.DateTimeField()),
                ('data_termino', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('descricao', models.CharField(max_length=50, default='Sem Descricao', null=True, blank=True, verbose_name='Descrição do Cargo')),
                ('horas_diarias', models.IntegerField(verbose_name='Horas Diárias', default=6)),
                ('salario', models.DecimalField(verbose_name='Salário', default=2000.0, max_digits=7, decimal_places=2)),
                ('tipo_cargo', models.CharField(max_length=10, default='Estágio', verbose_name='Tipo do Cargo', choices=[('Estágio', 'Estágio'), ('CLT', 'CLT')])),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sexo', models.CharField(max_length=1, default='M', verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])),
                ('nome', models.CharField(max_length=50, default='Sem Nome', verbose_name='Nome')),
                ('cpf', models.CharField(unique=True, max_length=11, default='Sem CPF', verbose_name='CPF')),
                ('telefone', models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='Telefone')),
                ('nascimento', models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)),
                ('Email', models.EmailField(max_length=30, default='', verbose_name='Email')),
                ('endereco', models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='Endereço')),
                ('cep', models.CharField(max_length=10, default='', null=True, blank=True, verbose_name='CEP')),
                ('caminho_foto', models.CharField(max_length=40, default='', null=True, blank=True, verbose_name='Caminho para a Foto')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('entrada', models.DateTimeField()),
                ('saida', models.DateTimeField(null=True, blank=True)),
                ('funcionario', models.ForeignKey(to='core.Funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='atribuicaocargo',
            name='cargo',
            field=models.ForeignKey(to='core.Cargo'),
        ),
        migrations.AddField(
            model_name='atribuicaocargo',
            name='funcionario',
            field=models.ForeignKey(to='core.Funcionario'),
        ),
    ]
