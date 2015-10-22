# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from . import Constraints as const

# Create your models here.
class Funcionario(models.Model):

    sexo = models.CharField(verbose_name="Sexo",
                            choices=const.SEXO_CHOICES,
                            max_length=1,
                            default=const.SEXO_CHOICES[0][0])

    nome = models.CharField(verbose_name="Nome",
                            max_length=50,
                            default=const.NOME_DEFAULT)

    cpf = models.CharField(verbose_name="CPF",
                           max_length=11,
                           default=const.CPF_DEFAULT,
                           unique=True)

    telefone = models.CharField(verbose_name="Telefone",
                                max_length=20,
                                default=const.VAZIO)

    email = models.EmailField(verbose_name="Email",
                              max_length=30,
                              default=const.VAZIO)

    endereço = models.CharField(verbose_name="Endereço",
                                max_length=20,
                                default=const.VAZIO)

    cep = models.CharField(verbose_name="CEP",
                           max_length=10,
                           default=const.VAZIO)

class Turno(models.Model):

    funcionario = models.ForeignKey(Funcionario)

    entrada = models.DateTimeField()

    saida = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.entrada = timezone.now()
        return super(Turno, self).save(*args, **kwargs)

class Cargo(models.Model):

    nome = models.CharField(verbose_name="Descrição do Cargo",
                            max_length=50,
                            default=const.NOME_DEFAULT)

    horas_diarias = models.IntegerField(verbose_name="Horas Diárias",
                                        default=const.HORAS_DIARIAS_DEFAULT)

    salario = models.DecimalField(verbose_name="Salário",
                                  decimal_places=2,
                                  max_digits=7,
                                  default=const.SALARIO_DEFAULT)

    tipo_cargo = models.CharField(verbose_name="Tipo do Cargo",
                                  max_length=10,
                                  choices=const.TIPO_CARGO_CHOICES,
                                  default=const.TIPO_CARGO_CHOICES[0][0])

class AtribuicaoCargo(models.Model):

    funcionario = models.ForeignKey(Funcionario)

    cargo = models.ForeignKey(Cargo)

    data_inicio = models.DateTimeField()

    data_termino = models.DateTimeField()




