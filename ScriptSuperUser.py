__author__ = 'felipe'
from core.models import Funcionario

Funcionario.objects.create_superuser(username='pbd',password='projetobd', email='pdb@cin.ufpe.br')

