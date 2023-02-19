import random
import time
from funcionario import Funcionario
from chave import *

def criar_base_de_dados(nome_arquivo: str):
  try:
    id_list = [i for i in range(5000)]
    arq = open(nome_arquivo + ".dat", "wb")
    i = 0
    
    while i < 5000:
      func = Funcionario(id = random.choice(id_list))
      id_list.remove(func.id)
      arq.write(bin(func.id)[2:].encode())
      arq.write("|".encode())
      arq.write(func.nome.encode())
      arq.write("|".encode())
      arq.write(func.cpf.encode())
      arq.write("|".encode())
      arq.write(func.data_nascimento.encode())
      arq.write("|".encode())
      arq.write(str(func.salario).encode())
      arq.write("#".encode())
      i += 1
  except(IOError):
    print(IOError)
    exit(1)
  print("Foi criada uma base de dados desordenada.")
  
  arq.close()

def le(file_name, seek=0):
  arq = open(file_name + ".dat", "rb")
  registro = ""
  arq.seek(seek)
  hash_seek = 1
  byte = arq.read(1).decode()

  while byte:
    if byte == "#":
      hash_seek += len(registro) + seek
      return registro, hash_seek
    registro += byte
    byte = arq.read(1).decode()

  arq.close()
  return registro, hash_seek

def le_registro_especifico(nome_arquivo: str, posicao_registro):
  with open(nome_arquivo + ".dat", "rb") as arq:
    cont_registro = 0
    byte = arq.read(1).decode()
    registro = ""
    encontrado = False
    campo = ""

    while cont_registro <= posicao_registro:
      registro += byte
      campo += byte
      if campo == bin(posicao_registro)[2:] + "|":
        encontrado = True
      if byte == "#":
        cont_registro += 1
        if encontrado:
          arq.close()
          return registro[:-1]
        registro = ""
        campo = ""
      if byte == "|":
        campo = ""
      byte = arq.read(1).decode()
  arq.close()

def tamanho(nome_arquivo: str):
  arq = open(nome_arquivo + ".dat", "r")
  num_registros = 0
  byte = arq.read(1)
  while byte:
    if byte == "#":
      num_registros += 1
    byte = arq.read(1)
  arq.close()
  return num_registros

def registro_para_memoria(registro: str):
  campos = registro.split("|")
  func = Funcionario(int(campos[0], 2), campos[1], campos[2], campos[3], float(campos[4]))
  return func

def busca_sequencial(nome_arquivo: str, chave: int):
  inicio = time.time()
  arq = open(nome_arquivo + ".dat", "rb")
  print(f"Pesquisando o funcionário {chave} por busca sequencial...")
  comparacoes = 0
  byte = arq.read(1).decode()
  registro = ""
  campo = ""
  search_id = bin(chave)[2:]
  encontrado = False

  while byte:
    campo += byte
    registro += byte
    if campo == search_id + "|":
      encontrado = True
    if byte == "#":
      comparacoes += 1
      if encontrado:
        arq.close()
        return registro[:-1], comparacoes, (time.time() - inicio)
      registro = ""
      campo = ""
    if byte == "|":
      campo = ""

    byte = arq.read(1).decode()
  arq.close()
  return None, comparacoes, (time.time() - inicio)

def insertion_sort(nome_arquivo: str):
  inicio = time.time()
  tam = tamanho(nome_arquivo)
  arq = open(nome_arquivo + ".dat", "r")
  chaves = [Chave() for _ in range(tam)]
  pos_registro = 0
  pos_seek = 0
  registro = ""
  
  while pos_registro < tam:
    arq.seek(pos_seek)
    registro, pos_seek = le(nome_arquivo, pos_seek)
    chaves[pos_registro].posicao = arq.tell()
    id = int(registro.split("|")[0], 2)
    chaves[pos_registro].chave_id = id
    pos_registro += 1

  chaves.sort(key=lambda x: x.chave_id)

  arq_ordenado = open(nome_arquivo + "_ordenado.dat", "wb")
  for k in range(tam):
    registro, _ =le(nome_arquivo, chaves[k].posicao)
    arq_ordenado.write(registro.encode() + "#".encode())
  
  arq.close()
  arq_ordenado.close()
  return time.time() - inicio

def busca_binaria(nome_arquivo: str, chave: int):
  inicio = time.perf_counter()
  comparacoes = 0
  arq = open(nome_arquivo + "_ordenado.dat", "rb")
  inicio = 0
  fim = tamanho(nome_arquivo) - 1
  arq.seek(0, 0)
  registro = ""

  while inicio <= fim:
    meio = (inicio + fim) // 2
    registro = le_registro_especifico(nome_arquivo + "_ordenado", meio)
    id_registro = int(registro.split("|")[0], 2)
    if id_registro == chave:
      comparacoes += 1
      return registro, comparacoes, (time.perf_counter() - inicio)
    elif chave < id_registro:
      fim = meio - 1
    elif chave > id_registro:
      inicio = meio + 1
    comparacoes += 1
  return None, comparacoes, (time.perf_counter() - inicio)

def selecao_substituicao(nome_arquivo: str):
  cont_particao = 1
  pos_seek = 0
  registro = ""
  M = [Funcionario() for _ in range(100)]
  arq = open(nome_arquivo + ".dat", "rb")
  for i in range(len(M)):
    arq.seek(pos_seek)
    registro, pos_seek = le(nome_arquivo, pos_seek)
    M[i] = registro_para_memoria(registro)
  saida = open("particoes/saida" + str(cont_particao) + ".dat", "wb")

  while M != []:
    todos_congelados = True
    for i in range(len(M)):
      if not M[i].congelado:
        todos_congelados = False
        menor_id = M[i].id
        menor = M[i]
        menor_pos = i
        break
    if not todos_congelados:
      for j in range(len(M)):
        if M[j].id < menor_id and not M[j].congelado:
          menor_id = M[j].id
          menor = M[j]
          menor_pos = j
      
      saida.write(bin(menor.id)[2:].encode())
      saida.write("|".encode())
      saida.write(menor.nome.encode())
      saida.write("|".encode())
      saida.write(menor.cpf.encode())
      saida.write("|".encode())
      saida.write(menor.data_nascimento.encode())
      saida.write("|".encode())
      saida.write(str(menor.salario).encode())
      saida.write("#".encode())
      
      if pos_seek != 1:
        arq.seek(pos_seek)
        registro, pos_seek = le(nome_arquivo, pos_seek)
      else:
        registro = ""
      if registro != "":
        M[menor_pos] = registro_para_memoria(registro)
        if M[menor_pos].id < menor.id:
          M[menor_pos].congelado = True
      else:
        M.remove(menor)

    else:
      saida.close()
      cont_particao += 1
      saida = open("particoes/saida" + str(cont_particao) + ".dat", "wb")
      for k in M:
        k.congelado = False
  
  saida.close()
  arq.close()

