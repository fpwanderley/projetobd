from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import datetime

INACTIVE_USER = 'O usuário está inativo.'
WRONG_USERNAME_OR_PASSWORD = 'Usuário e senha não conferem.'

@login_required
def home(request):

    if request.method == 'POST':
        check = request.POST['check']
        username = request.user.username

        funcionario = Funcionario.get_por_username(username)

        if funcionario.has_turno_aberto():
            funcionario.finalizar_turno()
        else:
            funcionario.iniciar_turno()

    usuario_logado = Funcionario.get_por_username(request.user.username)
    dia_atual = datetime.now().date()
    dia_atual_string = dia_atual.strftime('%d/%m/%Y')
    turnos_do_dia_do_usuario = Turno.turnos_por_funcionario_data(usuario_logado, data=dia_atual)
    total_trabalhado_hoje = Turno.calcula_horas_turnos(turnos_do_dia_do_usuario)
    horario_esperado = AtribuicaoCargo.get_horario_esperado_por_funcionario(funcionario=usuario_logado)
    estado_usuario = usuario_logado.has_turnos_abertos_data(dia_atual)
    horas_faltando = usuario_logado.calcula_total_horas_dia_faltando(data=dia_atual)
    previsao_horario_saida = usuario_logado.calcula_previsao_saida(data=dia_atual)
    usuario_admin = usuario_logado.is_superuser

    context = RequestContext(request,{
        'usuario': usuario_logado,
        'dia_atual': dia_atual_string,
        'turnos_do_dia': turnos_do_dia_do_usuario,
        'total_trabalhado': total_trabalhado_hoje,
        'horario_esperado': horario_esperado,
        'estado_usuario': estado_usuario,
        'horas_faltando': horas_faltando,
        'previsao_saida': previsao_horario_saida,
        'adm': usuario_admin
    })

    return render_to_response('index.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('core:login')

def user_login(request, next = None):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not next:
                    return redirect('core:home')
                else:
                    return redirect(next)

            else:
                error_message = INACTIVE_USER
        else:
            error_message = WRONG_USERNAME_OR_PASSWORD

        login_form = LoginForm()

        # Redireciona para a tela de login com mensagem de erro.
        context = RequestContext(request, {
            'error_message': error_message,
            'LoginForm':login_form,
        })
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context))

    else:
        next = ""
        if request.GET:
            next = request.GET['next']

        login_form = LoginForm()

        context = RequestContext(request, {
            'next': next,
            'LoginForm':login_form,
        })
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context))

@login_required()
def user_checkin(request):

    user = request.user

    user.iniciar_turno()

@login_required()
def user_report(request):
    from .AuxiliarClasses import Semana

    usuario_logado = Funcionario.get_por_username(request.user.username)

    if request.method == 'POST':
        pass

    else:
        dados_semana_atual = Semana()

        context = RequestContext(request,{
            'usuario': usuario_logado,
        })

        return render_to_response('report.html', context)


