def criar_lista_tuplos(dataset_file):
    lista_tuplos = []
    with open(dataset_file, 'r', encoding='utf-8') as file:
        for line in file:
            expressao, valor = line.strip().split(' : ')
            lista_tuplos.append((expressao, float(valor)))
    return lista_tuplos

def encontrar_correspondencias(text_file, lista_tuplos):
    with open(text_file, 'r', encoding='utf-8') as file:
        texto = file.read()

    texto = texto.lower()
    texto = texto.replace('.', '').replace(',', '')

    palavras = texto.split()
    correspondencias = []
    expressoes_encontradas = set()

    i = 0
    while i < len(palavras):
        for j in range(len(palavras), i, -1):
            expressao_composta = '_'.join(palavras[i:j])
            for expressao, pontuacao in lista_tuplos:
                if expressao_composta == expressao:
                    correspondencias.append((expressao_composta, pontuacao))
                    expressoes_encontradas.update(palavras[i:j])
                    i = j - 1
                    break
        i += 1

    for palavra in palavras:
        if palavra not in expressoes_encontradas:
            for expressao, pontuacao in lista_tuplos:
                if palavra == expressao:
                    correspondencias.append((palavra, pontuacao))

    return correspondencias

dataset = 'merged_dataset2.txt'
lista_tuplos = criar_lista_tuplos(dataset)

text_file = 'text.txt'
correspondencias = encontrar_correspondencias(text_file, lista_tuplos)

print("Correspondências encontradas:")
for palavra, pontuacao in correspondencias:
    print(f"{palavra} : {pontuacao}")
