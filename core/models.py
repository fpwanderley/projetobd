# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from . import Constraints as const
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.
class Funcionario(User):

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
                                default=const.VAZIO,
                                blank=True,
                                null=True)

    # Email criado com CamelCase por conta de atributo de mesmo nome na classe User.
    Email = models.EmailField(verbose_name="Email",
                              max_length=30,
                              default=const.VAZIO)

    endereco = models.CharField(verbose_name="Endereço",
                                max_length=20,
                                default=const.VAZIO,
                                blank=True,
                                null=True)

    cep = models.CharField(verbose_name="CEP",
                           max_length=10,
                           default=const.VAZIO,
                           blank=True,
                           null=True)

    caminho_foto = models.CharField(verbose_name="Caminho para a Foto",
                                    max_length=40,
                                    default=const.VAZIO,
                                    blank=True,
                                    null=True)
    def has_turno_aberto(self):
        if Turno.turnos_abertos_por_funcionario(funcionario=self):
            return True
        else:
            return False

    def iniciar_turno(self):

        if not self.has_turno_aberto:
            novo_turno = Turno(funcionario = self)
            novo_turno.save()
        else:
            # Retorna erro.
            pass

    def finalizar_turno(self):
        ultimo_turno_aberto = Turno.ultimo_turno_aberto_por_funcionario(funcionario=self)
        ultimo_turno_aberto.finalizar_turno()

    def calcula_total_horas_dia(self, dia):
        turnos_do_dia = Turno.turnos_fechados_por_funcionario_dia(funcionario=self, dia=dia)
        total_de_horas = Turno.calcula_horas_turnos(turnos=turnos_do_dia)
        return total_de_horas

class Turno(models.Model):

    funcionario = models.ForeignKey(Funcionario)

    entrada = models.DateTimeField()

    saida = models.DateTimeField(null=True)

    @classmethod
    def turnos_por_funcionario(cls, funcionario):
        return cls.objects.filter(funcionario = funcionario)

    @classmethod
    def turnos_abertos_por_funcionario(cls, funcionario):
        todos_turnos = cls.turnos_por_funcionario(funcionario=funcionario)
        turnos_abertos = [turno for turno in todos_turnos if (not turno.saida and turno.entrada)]
        return turnos_abertos

    @classmethod
    def turnos_fechados_por_funcionario(cls, funcionario):
        todos_turnos = cls.turnos_por_funcionario(funcionario=funcionario)
        turnos_fechados = [turno for turno in todos_turnos if (turno.saida and turno.entrada)]
        return turnos_fechados

    @classmethod
    def turnos_fechados_por_funcionario_dia(cls, funcionario, dia):
        turnos_fechados_funcionario = cls.turnos_fechados_por_funcionario(funcionario=funcionario)
        turnos_fechados_funcionario_dia = [turno for turno in turnos_fechados_funcionario if turno.saida.day == dia]
        return turnos_fechados_funcionario_dia

    @classmethod
    def ultimo_turno_aberto_por_funcionario(cls, funcionario):
        ultimo_turno = list(cls.turnos_por_funcionario(funcionario=funcionario))[-1]
        return ultimo_turno

    @classmethod
    def has_turno_aberto(cls, turnos):
        turnos_statuses = [True if turno.is_open() else False for turno in turnos]
        if any(turnos_statuses):
            return True
        else:
            return False

    @classmethod
    def calcula_horas_turnos(cls, turnos):

        if not cls.has_turno_aberto(turnos=turnos):
            total_segundos = float()

            for turno in turnos:
                total_segundos += turno.horas_trabalho().total_seconds()

            horas, segundos_restantes = divmod(total_segundos, 3600)
            minutos, segundos_restantes = divmod(segundos_restantes, 60)
            segundos = segundos_restantes

            import pdb;pdb.set_trace()

            return {
                'horas': int(horas),
                'minutos': int(minutos),
                'segundos': int(segundos)
            }

        else:
            # Retorna erro
            pass

    def is_open(self):
        if self.entrada and not self.saida:
            return True
        else:
            return False

    def finalizar_turno(self):
        if not self.saida:
            self.saida = timezone.now()
            self.save()
        else:
            # Retorna erro.
            pass

    def horas_trabalho(self):
        return self.saida - self.entrada

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.entrada = timezone.now()
        return super(Turno, self).save(*args, **kwargs)

class Cargo(models.Model):

    descricao = models.CharField(verbose_name="Descrição do Cargo",
                                 max_length=50,
                                 default=const.DESCRICAO_DEFAULT,
                                 blank=True,
                                 null=True)

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

    def __str__(self):
        return self.tipo_cargo + ': ' + self.descricao

class AtribuicaoCargo(models.Model):

    funcionario = models.ForeignKey(Funcionario)

    cargo = models.ForeignKey(Cargo)

    data_inicio = models.DateTimeField()

    data_termino = models.DateTimeField()




