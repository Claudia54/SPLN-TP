import jinja2
import os

def generate_template_from_metadata(metadata, output_dir):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('metadata_template.j2')
    rendered_content = template.render(metadata)

    # Write rendered content to file
    output_file = os.path.join(output_dir, 'generated_files.txt')
    with open(output_file, 'w') as f:
        f.write(rendered_content)

# Exemplo de uso
metadata = {
    'files': {
        'arquivo1.txt': 'Conteúdo do arquivo 1',
        'arquivo2.txt': 'Conteúdo do arquivo 2',
        # Adicione mais arquivos conforme necessário
    }
}
output_dir = 'output'
generate_template_from_metadata(metadata, output_dir)
