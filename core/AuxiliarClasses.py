from django.utils import timezone
from datetime import date, timedelta, datetime

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

    day_iso_format = day.date().isoformat()

    for week_number, week_days in weeks.items():

        if day_iso_format in week_days:
            week_days_date = [isoformat_to_date(week_day) for week_day in week_days]
            return week_number, week_days_date

def isoformat_to_date(isoformat_string):
    date = datetime.strptime(isoformat_string, '%Y-%m-%d').date()
    return date

def get_week_by_day(day):

    if not day:
        day = timezone.now()

    year = day.year

    all_weeks_of_year = get_weeks_by_year(year = year)

    week_number, week_days = find_day_in_week(day = day, weeks=all_weeks_of_year)

    return week_number, week_days

class Semana(object):

    def __init__(self, dia_inicio = None, dia_final = None):

        if (dia_inicio != None) and (dia_final != None):
            pass

        # Considerar a semana atual.
        else:
            dia_atual = timezone.now()
            self.number, self.days = get_week_by_day(day = dia_atual)

    def dados_semana_usuario_contexto(self, usuario_logado):
        dados_diarios = []

        for dia in self.days:
            dados_diario = {}
            dados_diario['date'] = dia
            dados_diario['total_horas'] = usuario_logado.calcula_total_horas_dia(data = dia)
            dados_diarios.append(dados_diario)

        return dados_diarios










