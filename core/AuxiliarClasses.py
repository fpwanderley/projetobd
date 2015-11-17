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

    month_iso_format = str(ano) + '-' + str(month) + '-'

    selected_weeks = []
    for week_number, week_days in weeks.items():

        if any([day for day in week_days if month_iso_format in day]):

            week_days_date = [isoformat_to_date(week_day) for week_day in week_days]
            week = week_days_date
            selected_weeks.append(week)

    return selected_weeks

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

def get_month_weeks_by_name(month_name):

    mes_atual = timezone.now().date().month
    mes_desejado = MONTH_NAME_TO_INTEGER[month_name]
    ano_desejado = timezone.now().date().year

    if mes_desejado > mes_atual:
        ano_desejado = ano_desejado - 1

    all_weeks_of_year = get_weeks_by_year(year = ano_desejado)

    weeks = find_weeks_in_a_month(month=mes_desejado, ano=ano_desejado,  weeks=all_weeks_of_year)

    return weeks


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

    def __init__(self, month_name = None):

        self.weeks = get_month_weeks_by_name(month_name = month_name)

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








