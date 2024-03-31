def create_bd():
    bd = {}
    try:
        with open("merged_dataset.txt", 'r') as file:
            content = file.read()
            linhas = content.split('\n')
            for line in linhas[:-1]:
                word, value = line.strip().split(' : ')
                #print(f"{word} | {float(value)}")
                bd[word] = float(value) 
    except FileNotFoundError:
        print(f"File not found.")
    return bd

bd = create_bd()


def encontrar_correspondencias(text_file):
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
            for expressao, pontuacao in bd.items():
                if expressao_composta == expressao:
                    correspondencias.append((expressao_composta, pontuacao))
                    expressoes_encontradas.update(palavras[i:j])
                    i = j - 1
                    break
        i += 1

    for palavra in palavras:
        if palavra not in expressoes_encontradas:
            for expressao, pontuacao in bd.items():
                if palavra == expressao:
                    correspondencias.append((palavra, pontuacao))

    return correspondencias

text_file= "Capitulos/Capitulo1.txt"


correspondencias = encontrar_correspondencias(text_file)

print("Correspondências encontradas:")
for palavra, pontuacao in correspondencias:
    print(f"{palavra} : {pontuacao}")