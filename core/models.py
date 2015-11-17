# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from . import Constraints as const
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date

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

    nascimento = models.DateField(verbose_name="Data de Nascimento",
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
    def get_cargo_atual(self):
        ultima_atribuicao = AtribuicaoCargo.get_ultima_atribuicao_aberta_por_funcionario(
            funcionario=self)

        return ultima_atribuicao.cargo.tipo_cargo + ': ' + ultima_atribuicao.cargo.descricao
    get_cargo_atual.short_description = 'Cargo Atual'

    @classmethod
    def get_por_username(cls, username):
        return cls.objects.get(username = username)

    def has_turno_aberto(self):
        if Turno.turnos_abertos_por_funcionario(funcionario=self):
            return True
        else:
            return False

    def deve_hora_dia(self, data):
        total_horas = self.calcula_total_horas_dia(data=data)['horas']
        horas_esperadas = AtribuicaoCargo.get_horario_esperado_por_funcionario(funcionario=self)

        if total_horas < horas_esperadas:
            return True
        else:
            return False


    def get_turno_aberto(self):
        return Turno.turnos_abertos_por_funcionario(funcionario=self)[0]

    def iniciar_turno(self):

        if not self.has_turno_aberto():
            novo_turno = Turno(funcionario = self)
            novo_turno.save()
        else:
            # Retorna erro.
            pass

    def finalizar_turno(self):
        ultimo_turno_aberto = Turno.ultimo_turno_aberto_por_funcionario(funcionario=self)
        ultimo_turno_aberto.finalizar_turno()

    def calcula_total_horas_dia(self, data):
        # import pdb;pdb.set_trace()
        turnos_do_dia = Turno.turnos_fechados_por_funcionario_dia(funcionario=self, data=data)

        if self.has_turno_aberto():
            turno_aberto = self.get_turno_aberto()
            turno_aberto.saida = timezone.now()
            turnos_do_dia.append(turno_aberto)

        total_de_horas = Turno.calcula_horas_turnos(turnos=turnos_do_dia)
        return total_de_horas

    def calcula_total_horas_dia_faltando(self, data):
        from datetime import timedelta
        total_de_horas_dia = self.calcula_total_horas_dia(data=data)

        horas_esperadas = AtribuicaoCargo.get_horario_esperado_por_funcionario(funcionario=self)
        timedelta_horas_esperadas = timedelta(hours=horas_esperadas)

        horas = total_de_horas_dia['horas']
        minutos = total_de_horas_dia['minutos']
        segundos = total_de_horas_dia['segundos']
        timedelta_horas_horas_trabalhadas = timedelta(hours=horas, minutes=minutos, seconds=segundos)

        horas_faltando = timedelta_horas_esperadas - timedelta_horas_horas_trabalhadas

        timedelta_dict = timedelta_to_dict(horas_faltando)

        return timedelta_dict

    def calcula_previsao_saida(self, data):
        horas_faltando = self.calcula_total_horas_dia_faltando(data=data)
        horas_faltando_timedelta = timedelta(hours = horas_faltando['horas'],
                                             minutes = horas_faltando['minutos'],
                                             seconds = horas_faltando['segundos'])

        hora_atual = timezone.now()
        previsao = hora_atual + horas_faltando_timedelta

        timedelta_dict = datetime_to_dict(previsao)

        return timedelta_dict

    def has_turnos_abertos_data(self, data):
        turnos_data = Turno.turnos_por_funcionario_data(funcionario = self, data = data)

        if Turno.has_turno_aberto(turnos_data):
            return True
        else:
            return False

    def get_last_12_months_of_work(self):

        def is_after(current_month, data_inicial):
            current_year = current_month.year
            current_month = current_month.month

            data_inicial_year = data_inicial.year
            data_inicial_month = data_inicial.month

            # Ano atual ainda esta depois do ano inicial.
            if current_year > data_inicial_year:
                return True
            elif current_year == data_inicial_year:
                if current_month >= data_inicial_month:
                    return True
                else:
                    return False

            # Ano Atual esta antes do ano inicial
            else:
                return False

        def before_month_date(current_month):
            month = current_month.month
            year = current_month.year

            if month == 1:
                next_month = 12
                next_year = year - 1

            else:
                next_month = month - 1
                next_year = year

            before_date = date(next_year, next_month, 1)
            return before_date

        def month_number_to_string_tuple(month_number_list):
            MONTH_TUPLES = {
                1: ('jan','Janeiro'),
                2: ('fev','Fevereiro'),
                3: ('mar','Março'),
                4: ('abr','Abril'),
                5: ('mai','Maio'),
                6: ('jun','Junho'),
                7: ('jul','Julho'),
                8: ('ago','Agosto'),
                9: ('set','Setembro'),
                10: ('out','Outubro'),
                11: ('nov','Novembro'),
                12: ('dez','Dezembro'),
            }

            return [MONTH_TUPLES[month] for month in month_number_list]

        todas_atribuicoes_ordenadas = AtribuicaoCargo.get_todas_atribuicoes_por_funcionario(funcionario=self).order_by('data_inicio')

        data_inicial = todas_atribuicoes_ordenadas[0].data_inicio.date()
        data_final = timezone.now().date()

        months = []
        current_month = data_final

        while (is_after(current_month=current_month,data_inicial=data_inicial) and len(months) <= 12):

            month_tuple = (current_month.month, current_month.year)
            months.append(month_tuple)
            current_month = before_month_date(current_month=current_month)

        list_of_months, list_of_years = map(list, zip(*months))
        list_of_months = month_number_to_string_tuple(month_number_list=list_of_months)

        return list_of_months, list_of_years

class Turno(models.Model):

    funcionario = models.ForeignKey(Funcionario)

    entrada = models.DateTimeField()

    saida = models.DateTimeField(blank=True,
                                 null=True)

    @classmethod
    def turnos_por_funcionario(cls, funcionario):
        return cls.objects.filter(funcionario = funcionario)

    @classmethod
    def turnos_por_funcionario_data(cls, funcionario, data):
        turnos_funcionario = cls.objects.filter(funcionario = funcionario)
        turnos_por_funcionario_data = [turno for turno in turnos_funcionario if turno.entrada.date() == data]
        return turnos_por_funcionario_data

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
    def turnos_fechados_por_funcionario_dia(cls, funcionario, data):
        turnos_fechados_funcionario = cls.turnos_fechados_por_funcionario(funcionario=funcionario)
        # import pdb;pdb.set_trace()
        turnos_fechados_funcionario_dia = [turno for turno in turnos_fechados_funcionario if turno.saida.date() == data]
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

        # Filtra os turnos fechados.
        turnos_fechados = [turno for turno in turnos if not turno.is_open()]

        total_segundos = float()

        for turno in turnos_fechados:
            total_segundos += turno.horas_trabalho().total_seconds()

        horas, segundos_restantes = divmod(total_segundos, 3600)
        minutos, segundos_restantes = divmod(segundos_restantes, 60)
        segundos = segundos_restantes

        return {
            'horas': int(horas),
            'minutos': int(minutos),
            'segundos': int(segundos)
        }

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

    data_termino = models.DateTimeField(blank=True,
                                        null=True)

    @classmethod
    def get_todas_atribuicoes_por_funcionario(cls, funcionario):
        return cls.objects.filter(funcionario = funcionario)

    @classmethod
    def get_atribuicoes_abertas_por_funcionario(cls, funcionario):
        todas_atribuicoes = cls.get_todas_atribuicoes_por_funcionario(funcionario=funcionario)
        return [atribuicao for atribuicao in todas_atribuicoes if atribuicao.is_open()]

    @classmethod
    def get_ultima_atribuicao_aberta_por_funcionario(cls, funcionario):
        todas_atribuicoes_abertas = cls.get_atribuicoes_abertas_por_funcionario(funcionario=funcionario)
        return todas_atribuicoes_abertas[-1]

    @classmethod
    def get_horario_esperado_por_funcionario(cls, funcionario):
        ultima_atribuicao = cls.get_ultima_atribuicao_aberta_por_funcionario(funcionario=funcionario)
        return ultima_atribuicao.cargo.horas_diarias

    def is_open(self):
        if self.data_inicio and not self.data_termino:
            return True
        else:
            return False

def timedelta_to_dict(timedelta_obj):
    total_segundos = timedelta_obj.total_seconds()

    horas, segundos_restantes = divmod(total_segundos, 3600)
    minutos, segundos_restantes = divmod(segundos_restantes, 60)
    segundos = segundos_restantes

    return {
        'horas': int(horas),
        'minutos': int(minutos),
        'segundos': int(segundos)
    }

def datetime_to_dict(datetime_obj):

    horas = datetime_obj.hour
    minutos = datetime_obj.minute
    segundos = datetime_obj.second

    return {
        'horas': int(horas),
        'minutos': int(minutos),
        'segundos': int(segundos)
    }


