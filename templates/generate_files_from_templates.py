from jinja2 import Template

# Generate the HTML file
with open('template_index.html') as f:
    template = Template(f.read())
with open('../index.html', 'w') as f:
    f.write(template.render())

# Generate the JS plotting scripts
with open('template_script.js') as f:
    template = Template(f.read())
with open('../script.js', 'w') as f:
    f.write(template.render())
