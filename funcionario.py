import string
import random

class Funcionario:

  def __init__(self, id: int, nome: str = "", cpf: str = "", data_nascimento: str = "", salario: float = 0) -> None:
    self.id = id
    self.nome = nome
    self.cpf = cpf
    self.data_nascimento = data_nascimento
    self.salario = salario
    self.criar_funcionario()

  def criar_funcionario(self):
    self.nome = "".join(random.choice(string.ascii_lowercase) for _ in range(50))
    self.cpf = self.cpf_formatado()
    self.data_nascimento = self.data_formatada()
    self.salario = round(random.uniform(0, 15000), 2)

  def data_formatada(self) -> str:
    dia = str(random.randint(1, 30))
    mes = str(random.randint(1, 12))
    ano = str(random.randint(1950, 2005))
    return dia + "/" + mes + "/" + ano

  def cpf_formatado(self):
    num_cpf = "".join(random.choice(string.digits) for _ in range(11))
    return num_cpf[0:3] + "." + num_cpf[3:6] + "." + num_cpf[6:9] + "-" + num_cpf[9:11]

