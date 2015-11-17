from django.utils import timezone
from datetime import date, timedelta, datetime

DAY_NUMBER = {
    1: 'Domingo',
    2: 'Segunda-Feira',
    3: 'Terça-Feira',
    4: 'Quarta-Feira',
    5: 'Quinta-Feira',
    6: 'Sexta-Feira',
    7: 'Sábado',
}

MONTH_NAME_TO_INTEGER ={
    'jan':1,
    'fev':2,
    'mar':3,
    'abr':4,
    'mai':5,
    'jun':6,
    'jul':7,
    'ago':8,
    'set':9,
    'out':10,
    'nov':11,
    'dez':12
}

VERDE = '#2CA044'
VERMELHO = '#D62728'

def allsundays(year):
    """This code was provided in the previous answer! It's not mine!"""
    d = date(year, 1, 1)                    # January 1st
    d += timedelta(days = 6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days = 7)

def get_weeks_by_year(year):
    Dict = {}
    for wn,d in enumerate(allsundays(year)):
        # This is my only contribution!
        Dict[wn+1] = [(d + timedelta(days=k)).isoformat() for k in range(0,7) ]

    return Dict

def find_day_in_week(day, weeks):

    if isinstance(day, datetime):
        day_iso_format = day.date().isoformat()
    else:
        day_iso_format = day.isoformat()

    for week_number, week_days in weeks.items():

        if day_iso_format in week_days:
            week_days_date = [isoformat_to_date(week_day) for week_day in week_days]
            return week_number, week_days_date

def find_weeks_in_a_month(month, ano, weeks):

    if month < 10:
        month_iso_format = str(ano) + '-0' + str(month) + '-'
    else:
        month_iso_format = str(ano) + '-' + str(month) + '-'

    selected_weeks = []
    for week_number, week_days in weeks.items():

        if any([day for day in week_days if month_iso_format in day]):

            week_days_date = [isoformat_to_date(week_day) for week_day in week_days]
            week = week_days_date
            selected_weeks.append(week)

    return selected_weeks

def find_months_in_a_year(ano,  weeks):

    year_iso_format = str(ano) + '-'

    year_days = []
    for week_number, week_days in weeks.items():
        for day in week_days:
            if (year_iso_format in day):
                year_days.append(day)

    months = {idx+1: [] for idx in range(12)}

    for day in year_days:
        month = int(day.split('-')[1])
        months[month].append(isoformat_to_date(day))

    month_list = [value for key, value in months.items()]
    return month_list

def isoformat_to_date(isoformat_string):
    date = datetime.strptime(isoformat_string, '%Y-%m-%d').date()
    return date

def postformat_to_date(isoformat_string):
    date = datetime.strptime(isoformat_string, '%d/%m/%Y').date()
    return date

def get_week_by_day(day):

    if not day:
        day = timezone.now()

    year = day.year

    all_weeks_of_year = get_weeks_by_year(year = year)

    week_number, week_days = find_day_in_week(day = day, weeks=all_weeks_of_year)

    return week_number, week_days

def total_horas_dict_to_float(total_horas):
    total_float = total_horas['horas'] + total_horas['minutos']/60 + total_horas['segundos']/3600
    return total_float

def get_month_weeks_by_name(month_name, ano_desejado = None):

    mes_atual = timezone.now().date().month
    mes_desejado = MONTH_NAME_TO_INTEGER[month_name]

    if not ano_desejado:
        ano_desejado = timezone.now().date().year

        if mes_desejado > mes_atual:
            ano_desejado = ano_desejado - 1

    all_weeks_of_year = get_weeks_by_year(year = ano_desejado)

    weeks = find_weeks_in_a_month(month=mes_desejado, ano=ano_desejado,  weeks=all_weeks_of_year)

    return weeks

def get_months_by_year(year):

    all_weeks_of_year = get_weeks_by_year(year = year)

    months = find_months_in_a_year(ano=year,  weeks=all_weeks_of_year)

    return months

def get_days_by_weeks(weeks):
    days = []
    for week in weeks:
        days = days + week
    return days

def get_days_by_months(months):
    days = []
    for month in months:
        days = days + month
    return days

class Dia(object):

    def __init__(self, usuarios, dia):

        self.usuarios = usuarios
        self.dia = dia

    def admin_dados_dia_usuarios_contexto(self):

        data = {}
        data['key'] = 'Relatório Diário'
        dados_diarios = []

        for idx, usuario in enumerate(self.usuarios):

            total_horas = usuario.calcula_total_horas_dia(data = self.dia)

            dados_diario = {}
            if usuario.deve_hora_dia(data = self.dia):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = usuario.nome
            dados_diario['value'] = total_horas_dict_to_float(total_horas)
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data

class Semana(object):

    def __init__(self, week_day = None):

        # Considerando a semana onde o week_day está incluso.
        if (week_day != None):
            dia_atual = week_day
            self.number, self.days = get_week_by_day(day = dia_atual)

        # Considerar a semana atual.
        else:
            dia_atual = timezone.now()
            self.number, self.days = get_week_by_day(day = dia_atual)

    def dados_semana_usuario_contexto(self, usuario_logado):

        data = {}
        data['key'] = 'Dias da semana'

        dados_diarios = []

        for idx, dia in enumerate(self.days):

            total_horas = usuario_logado.calcula_total_horas_dia(data = dia)

            dados_diario = {}
            if usuario_logado.deve_hora_dia(data=dia):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = DAY_NUMBER[idx+1]
            dados_diario['value'] = total_horas_dict_to_float(total_horas)
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data

class Mes(object):

    def __init__(self, month_name = None, year=None, usuarios=None):
        self.month = MONTH_NAME_TO_INTEGER[month_name]
        self.weeks = get_month_weeks_by_name(month_name = month_name, ano_desejado = year)
        self.usuarios = usuarios

    def dados_weeks_usuario_contexto(self, usuario_logado):

        data = {}
        data['key'] = 'Semanas do Mês'

        dados_diarios = []

        for idx, week in enumerate(self.weeks):

            total_horas = usuario_logado.calcula_total_horas_dias(datas = week)

            dados_diario = {}
            if usuario_logado.deve_hora_semana(total_horas=total_horas):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = 'Semana: ' + str(idx+1)
            dados_diario['value'] = total_horas
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data

    def admin_dados_mes_usuarios_contexto(self):

        data = {}
        data['key'] = 'Relatório Mensal'
        dados_diarios = []
        self.dias = get_days_by_weeks(weeks=self.weeks)

        for idx, usuario in enumerate(self.usuarios):

            total_horas = usuario.calcula_total_horas_dias(datas = self.dias)
            dias_uteis = self.retorna_dias_uteis()

            dados_diario = {}
            if usuario.deve_hora_dias(total_dias=self.dias, dias_uteis=dias_uteis):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = usuario.nome
            dados_diario['value'] = total_horas
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data

    def retorna_dias_uteis(self):

        dias_uteis = []
        for week in self.weeks:
            for dia in week:
                if (dia.month == self.month) and (dia.weekday() < 5):
                    dias_uteis.append(dia)
        return dias_uteis

class Ano(object):

    def __init__(self, year, usuarios):
        self.usuarios = usuarios
        self.year = year
        self.months = get_months_by_year(year = year)

    def dados_meses_usuario_contexto(self, usuario_logado):

        from .models import MONTH_TUPLES

        data = {}
        data['key'] = 'Meses do Ano'

        dados_diarios = []

        for idx, month in enumerate(self.months):

            total_horas = usuario_logado.calcula_total_horas_dias(datas = month)

            month_obj = Mes(month_name=MONTH_TUPLES[idx+1][0], year=self.year)
            dias_uteis = month_obj.retorna_dias_uteis()

            dados_diario = {}
            if usuario_logado.deve_hora_dias(total_dias=dias_uteis, dias_uteis=dias_uteis):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = MONTH_TUPLES[idx+1][0]
            dados_diario['value'] = total_horas
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data

    def admin_dados_ano_usuario_contexto(self):

        from .models import MONTH_TUPLES

        data = {}
        data['key'] = 'Relatório Anual'
        dados_diarios = []

        dias_uteis = []
        for idx, month in enumerate(self.months):
            month_obj = Mes(month_name=MONTH_TUPLES[idx+1][0], year=self.year)
            dias_uteis.append(month_obj.retorna_dias_uteis())

        self.dias = get_days_by_months(self.months)

        for idx, usuario in enumerate(self.usuarios):

            total_horas = usuario.calcula_total_horas_dias(datas = self.dias)

            dados_diario = {}
            if usuario.deve_hora_dias(total_dias=self.dias, dias_uteis=dias_uteis):
                dados_diario['color'] = VERMELHO
            else:
                dados_diario['color'] = VERDE
            dados_diario['label'] = usuario.nome
            dados_diario['value'] = total_horas
            dados_diarios.append(dados_diario)

        data['values'] = dados_diarios

        return data








