from jinja2 import Template

with open('template_index.html') as f:
    template = Template(f.read())

with open('../index.html', 'w') as f:
    f.write(template.render())
