
# coding: utf-8

# In[9]:


import bokeh
from bokeh.plotting import output_file, figure, show
from bokeh.embed import components
from jinja2 import Template


# In[10]:


import pandas as pd


# In[11]:


title_and_files = [ 
    ('Perf. single node', './logs_csv/per_n_nodes/cori_knl_alltests_nnode_1.csv'),
    ('Perf. two node', './logs_csv/per_n_nodes/cori_knl_alltests_nnode_1.csv') ]
plots = []
for title, file in title_and_files:
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'])
    # create a new plot with a datetime axis type
    p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
    p.line(df['date'], df['step_time'], color='navy', alpha=0.5)
    div, script = components(p)
    plots.append((title, div, script))


# In[4]:


# Generate the HTML file
with open('templates/template_index.html') as f:
    template = Template(f.read())
with open('index.html', 'w') as f:
    f.write(template.render(L=plots))

