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

    if not isinstance(day, date):
        day_iso_format = day.date().isoformat()
    else:
        day_iso_format = day.isoformat()

    for week_number, week_days in weeks.items():

        if day_iso_format in week_days:
            week_days_date = [isoformat_to_date(week_day) for week_day in week_days]
            return week_number, week_days_date

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










