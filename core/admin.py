from django.contrib import admin
from .models import Funcionario, Cargo, AtribuicaoCargo, Turno

# Register your models here.
@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'is_superuser', 'cpf')
    list_display_links = ('nome',)
    fieldsets = (
        ('Dados do Funcionario',{
            'fields': ('nome', 'cpf', 'sexo','Email','telefone', 'endereco', 'cep', 'caminho_foto')
        }),
        ('Opcoes Avancadas',{
            'fields': ('username', 'password','is_superuser', 'is_active', 'groups')
        }),
    )
    exclude = ('first_name','last_name','email')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('tipo_cargo', 'horas_diarias', 'salario', 'descricao')
    list_display_links = ('tipo_cargo',)
    fieldsets = (
        ('Dados do Cargo',{
            'fields': ('tipo_cargo', 'horas_diarias', 'salario', 'descricao')
        }),
    )

@admin.register(AtribuicaoCargo)
class AtribuicaoCargoAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'cargo', 'data_inicio', 'data_termino')
    list_display_links = ('funcionario',)
    fieldsets = (
        ('Dados da Atribuicao do Cargo',{
            'fields': ('funcionario', 'cargo', 'data_inicio', 'data_termino')
        }),
    )

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'entrada', 'saida')
    list_display_links = ('funcionario',)
    fieldsets = (
        ('Dados do Turno',{
            'fields': ('funcionario', 'entrada', 'saida')
        }),
    )