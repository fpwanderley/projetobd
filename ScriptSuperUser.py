from core.models import Funcionario, Cargo, AtribuicaoCargo
from datetime import timedelta, datetime

novo_cargo = Cargo(horas_diarias=8, salario=2000)
novo_cargo.save()

cargo_sem_cargo = Cargo(descricao='Sem Cargo', horas_diarias=0, salario=0)
cargo_sem_cargo.save()

pbd = Funcionario.objects.create_superuser(username='pbd',password='projetobd', email='pbd@cin.ufpe.br')

nova_atribuicao = AtribuicaoCargo(funcionario=pbd, cargo=novo_cargo, data_inicio=datetime.now())
nova_atribuicao.save()

