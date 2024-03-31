import jinja2
import os

def render_template(template_path, metadata, output_dir):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    rendered_content = template.render(metadata)

    # Create directories if they don't exist
    os.makedirs(output_dir, exist_ok=True)

    # Write rendered content to file
    output_file = os.path.join(output_dir, os.path.basename(template_path))
    with open(output_file, 'w') as f:
        f.write(rendered_content)

# Exemplo de uso
template_path = 'template.j2'
metadata = {
    'title': 'Exemplo de Template Jinja2',
    'heading': 'Bem-vindo ao Exemplo',
    'content': 'Este é um exemplo simples de como usar Jinja2 para renderizar templates.'
}
output_dir = 'output'
render_template(template_path, metadata, output_dir)
