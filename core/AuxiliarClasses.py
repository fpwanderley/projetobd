from django.utils import timezone

class Semana(object):

    def __init__(self, dia_inicio = None, dia_final = None):

        if (dia_inicio == None) and (dia_final == None):
            pass

        # Considerar a semana atual.
        else:
            dia_atual = timezone.now()



