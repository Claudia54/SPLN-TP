import json


# Função para dividir os números por 5 e adicionar aspas, se necessário
def process_value(value):
    # Converte para string se não for
    if not isinstance(value, str):
        value = str(value)
    # Verifica se o valor não está entre aspas e adiciona aspas
    if not value.startswith('"') and not value.endswith('"'):
        value = f'"{value}"'
    # Remove aspas e converte para número, depois divide por 5
    new_value = float(value.strip('"')) / 5
    return new_value

# Ler o arquivo JSON externo
with open('fixed_merged.json', 'r') as file:
    data = json.load(file)

# Processar os valores e criar um novo dicionário
new_data = {}
for word, value in data.items():
    new_data[word] = process_value(value)

# Escrever o novo dicionário em um novo arquivo JSON
with open('processed_fixed_merged.json', 'w') as file:
    json.dump(new_data, file, indent=2)
