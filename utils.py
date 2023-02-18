import random
import time
from funcionario import Funcionario
from chave import Chave

def criar_base_de_dados(nome_arquivo: str):
  try:
    id_list = [i for i in range(10)]
    arq = open(nome_arquivo + ".dat", "wb")
    i = 0
    
    while i < 10:
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
  print("Base de dados criada")
  
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

def busca_sequencial(nome_arquivo: str, chave: int):
  start = time.perf_counter()
  file = open(nome_arquivo + ".dat", "rb")
  print(f"Pesquisando o funcionário {chave} por busca sequencial...")
  comparisons = 0
  byte = file.read(1).decode()
  saved_register = ""
  field = ""
  search_id = bin(chave)[2:]
  finded = False

  while byte:
    field += byte
    saved_register += byte
    if field == search_id + "|":
      finded = True
      if byte == "#":
        comparisons += 1
        if finded:
          total_time = time.perf_counter() - start
          file.close()
          return saved_register[:-1], comparisons, total_time
        saved_register = ""
        field = ""
      if byte == "|":
        field = ""

    byte = file.read(1).decode()
  file.close()
  return None, comparisons, time.perf_counter() - start

def insertion_sort(nome_arquivo: str):
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

def busca_binaria(nome_arquivo: str, chave: int):
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
      return registro
    elif chave < id_registro:
      fim = meio - 1
    elif chave > id_registro:
      inicio = meio + 1
  return None