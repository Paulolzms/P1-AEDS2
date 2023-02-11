import random
import time
from funcionario import Funcionario

def criar_base_de_dados(nome_arquivo: str):
  try:
    id_list = [i for i in range(10)]
    arq = open(nome_arquivo, "w")
    i = 0
    
    while i < 10:
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

def busca_sequencial(nome_arquivo: str, chave: int):
  tempo_inicial = time.perf_counter()
  arq = open(nome_arquivo + ".txt", "r")
  registros = arq.readlines() 
  
  for i in range(len(registros)):
    registro = registros[i]
    codigo = ""    
    for j in range(len(registro)):
      if registro[j] == "|":
        if codigo == str(chave):
          arq.close()
          tempo_final = time.perf_counter() - tempo_inicial
          return registro, i+1, tempo_final
        else:
          break 
      codigo += registro[j]
  
  arq.close()


