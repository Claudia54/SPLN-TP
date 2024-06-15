import json

def create_bd():
    bd = {}
    try:
        with open("fixed_merged.json", 'r') as file:
            bd = json.load(file)
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
        for j in range(i+5, i, -1):
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
total = 0
for palavra, pontuacao in correspondencias:
    total += float(pontuacao)
    print(f"{palavra} : {pontuacao}")
print(f"total: {total}")
print(f"media do capitulo: {total/len(palavra)}")