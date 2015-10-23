# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtribuicaoCargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('data_inicio', models.DateTimeField()),
                ('data_termino', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Descrição do Cargo', default='Sem Nome', max_length=50)),
                ('horas_diarias', models.IntegerField(verbose_name='Horas Diárias', default=6)),
                ('salario', models.DecimalField(verbose_name='Salário', default=2000.0, decimal_places=2, max_digits=7)),
                ('tipo_cargo', models.CharField(verbose_name='Tipo do Cargo', default='Estágio', choices=[('Estágio', 'Estágio'), ('CLT', 'CLT')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('sexo', models.CharField(verbose_name='Sexo', default='M', choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('nome', models.CharField(verbose_name='Nome', default='Sem Nome', max_length=50)),
                ('cpf', models.CharField(verbose_name='CPF', default='Sem CPF', max_length=11, unique=True)),
                ('telefone', models.CharField(verbose_name='Telefone', default='', max_length=20)),
                ('email', models.EmailField(verbose_name='Email', default='', max_length=30)),
                ('endereço', models.CharField(verbose_name='Endereço', default='', max_length=20)),
                ('cep', models.CharField(verbose_name='CEP', default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('entrada', models.DateTimeField()),
                ('saida', models.DateTimeField()),
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
