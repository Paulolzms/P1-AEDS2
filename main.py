from utils import *

print("\nQuestão 1:")
nome_arquivo = input("Digite o nome do arquivo: ")
criar_base_de_dados(nome_arquivo)

print("\nQuestão 2:")
registro, comparacoes, tempo = busca_sequencial(nome_arquivo, int(input("Digite o id do funcionário à ser encontrado por busca sequencial: ")))
RegistroFormatado(registro, comparacoes, tempo, "Questão2/DadosFuncionario.txt")

op_invalida = True
while op_invalida:
  print("\n1-Insertion sort\n2-Ordenação externa")
  opcao = input(f"Escolha um método de ordenação: ")
  if int(opcao) == 1:
    print("\nQuestão 3:")
    print(f"Ordenando arquivo {nome_arquivo} pelo método insertion sort...\nTempo: {insertion_sort(nome_arquivo)}s")
    op_invalida = False
  elif int(opcao) == 2:
    print("\nQuestão 4: Não foi implementado a parte de intercalaçao")
    exit()
    op_invalida = False
  else:
    print("Opção inválida")

print("\nQuestão 5:")
registro, comparacoes, tempo = busca_binaria(nome_arquivo, int(input("Digite o id do funcionário à ser encontrado por busca binária: ")))
RegistroFormatado(registro, comparacoes, tempo, "Questão5/DadosFuncionario.txt")

