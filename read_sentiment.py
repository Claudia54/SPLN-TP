
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

'''
#Iterar sobre o texto e separa o mesmo em frases. Pondo cada palavra
#em lowecase.
def iterate_words_lowercase(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            sentences = content.split('.')
            for sentence in sentences:
                words = sentence.split()
                for word in words:
                    lowercase_word = word.lower()
                    print(lowercase_word)
                print()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

'''
# Split 
def iterate_words_frase(frase):   
    cont = ""
    sent = 0
    words = frase.split()
    for word in words:
        lowercase_word = word.lower()
        if not cont:
            cont = lowercase_word + "_"
        else:
            tenta = cont + lowercase_word
            print(tenta)
            if tenta in bd.keys():
                cont += lowercase_word + "_"
            else:
                word = cont[:-1]
                if word in bd.keys():
                    print(word)
                    print(bd[cont[:-1]])
                    sent += bd[word]
                cont = lowercase_word + "_"
    if cont[:-1] in bd.keys():
        print(bd[cont[:-1]])
        sent += bd[cont[:-1]]
                
    print(sent)
# Replace 'file_path' with the path to your file

iterate_words_frase("não perceberão patavina")



"""
Itera pelo texto, calcula o valor de cada frase e salva a frase e seu valor em um arquivo de saída.
"""
def calcular_e_salvar_valores(texto, arquivo_saida):
    with open(arquivo_saida, 'w') as f:
        frases = texto.split('.')  # Divide o texto em frases
        for frase in frases:
            valor_frase = iterate_words_frase(frase)
            f.write(f"Frase: {frase.strip()}\n")
            f.write(f"Valor: {valor_frase}\n\n")

# Exemplo de uso:
texto_grande = "Este é um exemplo de texto grande. Ele contém várias frases, algumas das quais podem ter palavras do nosso dicionário de pontuações. Vamos calcular o valor de cada frase e salvá-lo em um arquivo separado."
arquivo_saida = "frases_valores.txt"

#calcular_e_salvar_valores(texto_grande, arquivo_saida) 