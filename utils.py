import random
from funcionario import Funcionario

def criar_base_de_dados(nome_arquivo: str):
  try:
    id_list = [i for i in range(5000)]
    arq = open(nome_arquivo, "w")
    i = 0
    while i < 5000:
      func = Funcionario(id = random.choice(id_list))
      id_list.remove(func.id)
      arq.write(str(func.id))
      arq.write("|")
      arq.write(func.nome)
      arq.write("|")
      arq.write(func.cpf)
      arq.write("|")
      arq.write(func.data_nascimento)
      arq.write("|")
      arq.write(str(func.salario))
      arq.write("\n")
      i += 1
  except(IOError):
    print(IOError)
    exit(1)
  print("Base de dados criada")
  arq.close()