# -*- coding: UTF-8 -*-
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

DATE_REQUEST = 'date'
MONTH_REQUEST = 'month'
YEAR_REQUEST = 'year'

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
    dia_atual = timezone.now().date()
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
    from .AuxiliarClasses import Semana, postformat_to_date, Mes, Ano
    import json

    usuario_logado = Funcionario.get_por_username(request.user.username)
    usuario_admin = usuario_logado.is_superuser
    ultimos_12_meses, ultimos_anos = usuario_logado.get_last_12_months_of_work()

    if request.method == 'POST':
        request_type = request.POST['request_type']
        selected_date = request.POST['selected_date']
        print(request_type)
        print(selected_date)

        if (request_type == DATE_REQUEST):
            selected_day = postformat_to_date(selected_date)
            semana_atual = Semana(week_day=selected_day)
            dados_semana_contexto = semana_atual.dados_semana_usuario_contexto(usuario_logado=usuario_logado)

            # trocar o js data para o json.dumps() com o contexto correto de acordo com o request type e o selected date
            js_data = json.dumps(dados_semana_contexto)

        elif (request_type == MONTH_REQUEST):
            mes = Mes(month_name=selected_date)
            dados_mes_contexto = mes.dados_weeks_usuario_contexto(usuario_logado=usuario_logado)
            js_data = json.dumps(dados_mes_contexto)

        elif (request_type == YEAR_REQUEST):
            ano = Ano(year=int(selected_date))
            dados_ano_contexto = ano.dados_meses_usuario_contexto(usuario_logado=usuario_logado)
            js_data = json.dumps(dados_ano_contexto)

    else:
        semana_atual = Semana()
        dados_semana_contexto = semana_atual.dados_semana_usuario_contexto(usuario_logado=usuario_logado)

        js_data = json.dumps(dados_semana_contexto)

    context = RequestContext(request,{
        'usuario': usuario_logado,
        'data': js_data,
        'months': ultimos_12_meses,
        'years': ultimos_anos,
        'adm': usuario_admin
    })
    template = loader.get_template('report.html')
    return HttpResponse(template.render(context))



@login_required
def admin_report(request):
    from .AuxiliarClasses import Semana, postformat_to_date, Mes, Ano, Dia
    import json

    usuarios = Funcionario.get_all()
    usuario_logado = Funcionario.get_por_username(request.user.username)
    usuario_admin = usuario_logado.is_superuser
    ultimos_12_meses, ultimos_anos = usuario_logado.get_last_12_months_of_work()

    if request.method == 'POST':
        request_type = request.POST['request_type']
        selected_date = request.POST['selected_date']
        print(request_type)
        print(selected_date)

        if (request_type == DATE_REQUEST):
            selected_day = postformat_to_date(selected_date)
            dia_atual = Dia(dia=selected_day, usuarios=usuarios)
            dados_dia_contexto = dia_atual.admin_dados_dia_usuarios_contexto()

            # trocar o js data para o json.dumps() com o contexto correto de acordo com o request type e o selected date
            js_data = json.dumps(dados_dia_contexto)

        elif (request_type == MONTH_REQUEST):
            mes = Mes(month_name=selected_date, usuarios=usuarios)
            dados_mes_contexto = mes.admin_dados_mes_usuarios_contexto()

            js_data = json.dumps(dados_mes_contexto)

        elif (request_type == YEAR_REQUEST):
            ano = Ano(year=int(selected_date), usuarios=usuarios)
            dados_ano_contexto = ano.admin_dados_ano_usuario_contexto()

            js_data = json.dumps(dados_ano_contexto)

    else:
        selected_day = timezone.now().date()
        dia_atual = Dia(dia=selected_day, usuarios=usuarios)
        dados_dia_contexto = dia_atual.admin_dados_dia_usuarios_contexto()
        js_data = json.dumps(dados_dia_contexto)

    context = RequestContext(request,{
        'usuario': usuario_logado,
        'data': js_data,
        'months': ultimos_12_meses,
        'years': ultimos_anos,
        'adm': usuario_admin
    })
    template = loader.get_template('admin_report.html')
    return HttpResponse(template.render(context))