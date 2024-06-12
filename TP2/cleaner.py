import re

def process_sql_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Remove linhas que começam com SET
            if not line.startswith('SET'):
                # Remove 'public.' de INSERT INTO
                line = re.sub(r'INSERT INTO public\.(\w+)', r'INSERT INTO \1', line)
                outfile.write(line)

# Exemplo de uso:
input_file = 'dre_dump.sql'
output_file = 'dre_dump_processed.sql'
process_sql_file(input_file, output_file)
