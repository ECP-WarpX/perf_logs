import shutil, os
from bokeh.plotting import figure, gridplot, output_file, show
from bokeh.models import Legend
from bokeh.embed import components
from jinja2 import Template
import pandas as pd

dict_csv_files = {
    'Cori @ NERSC' : './logs_csv/cori_knl.csv',
    'Summit @ OLCF': './logs_csv/summit.csv'
    }

html_file = 'index.html'

# Generate the HTML file
with open('templates/template_index.html') as f:
    template = Template(f.read())
with open(html_file, 'w') as f:

    for machine in list( dict_csv_files.keys() ):

        csv_file = dict_csv_files[machine]

        print(machine, csv_file)

        df = pd.read_csv( csv_file )

        color_list = ('red', 'orange', 'green', 'blue', 'brown', 'gray')
        plots = []
        #################################################################################
        ### First part: for a given test, give performance history for several n_node ###
        #################################################################################
        node_list = [1, 8, 64, 512, 2048, 4096, 8192]
        # only keep n_node that are in df
        node_list = [ i for i in node_list if i <= df['n_node'].max() ]
        # Which quantities to plot on this dataframe
        x_axis = 'date'
        y_axis = 'step_time' 
        x_label = x_axis
        y_label = y_axis + ' (s)'
        # Prepare list of figures
        fig_list = []
        input_file_list = df['input_file'].unique()
        # Loop on input_file, i.e. different tests
        # One figure per test
        for count, input_file in enumerate( input_file_list ):
            df_filtered = df[ df['input_file']==input_file ]
            y_data_allmax = df_filtered[y_axis].max()
            fig = figure(width=250, plot_height=250, title=input_file.replace('automated_test_',''), 
                         x_axis_type="datetime", y_axis_type='log')
            # y_range=[0., 1.1*y_data_allmax], 
            # Ugly trick to have the legend outside the plot.
            # The last plot of the line is larger, and a fraction of 
            # it contains the legend...
            if count==len( input_file_list ) - 1: # this is test automated_test_6_output_2ppc 
                fig = figure(width=350, plot_height=250, title=input_file.replace('automated_test_',''), 
                             x_axis_type="datetime", y_axis_type='log')
            # Loop on n_node
            # All on the same figure different colors
            legend_it = [] # Trick to have legend outside the plot
            for inner_count, n_node in enumerate( node_list ):
                color = color_list[inner_count]
                x_data = pd.to_datetime(df_filtered[df_filtered['n_node']==n_node][x_axis])
                y_data = df_filtered[df_filtered['n_node']==n_node][y_axis]
                c = fig.circle(x_data, y_data, size=5, fill_color=color, line_color=color, alpha=.5)
                legend_it.append((str(n_node) + ' nodes', [c]))
            fig.xaxis.axis_label = x_label
            fig.yaxis.axis_label = y_label
            fig_list.append( fig )
        # For the legend ugly trick
        legend = Legend(items=legend_it, location=(0, 0))
        legend.click_policy="mute"
        fig.add_layout(legend, 'right')
        # Store each plot in a 2d, here we chose a single row 
        p1 = gridplot([ fig_list ])
        div, script = components(p1)
        # script, div = components( gridplot([ fig_list ]) )
        plots.append((machine + ' Performance history for each test', div, script))

        ################################################################################################
        ### Second part: for a given test, give the latest weak scaling on up to more that 512 nodes ###
        ################################################################################################
        # Get final run with max nnode >= 512
        max_start_date = df[df['n_node']>=2]['start_date'].max()
        df_filtered = df[df['start_date']==max_start_date]
        # Which quantities to plot on this dataframe
        x_axis = 'n_node' 
        y_axis = 'step_time' 
        x_label = x_axis
        y_label = y_axis + ' (s)'
        # Prepare list of figures
        fig_list = []
        # Loop on input_file, i.e. different tests
        # One figure per test
        for count, input_file in enumerate( df_filtered['input_file'].unique() ):
            color = color_list[count]
            x_data = df_filtered[df_filtered['input_file']==input_file][x_axis]
            y_data = df_filtered[df_filtered['input_file']==input_file][y_axis]
            fig = figure(width=250, plot_height=250, title=input_file.replace('automated_test_',''), 
                         y_range=[0., 1.1*y_data.max()], x_axis_type='log')
            # fig = figure(width=250, plot_height=250, title=input_file.replace('automated_test_',''), 
            #              x_axis_type='log', y_axis_type='log')
            fig.circle(x_data, y_data, size=5, fill_color=color, line_color=color, 
                       alpha=.5, legend=input_file.replace('automated_test_',''))
            fig.xaxis.axis_label = x_label
            fig.yaxis.axis_label = y_label
            fig_list.append( fig )
            fig.legend.location='bottom_right'
        # Store each plot in a 2d, here we chose a single row 
        p2 = gridplot([ fig_list ])
        div, script = components(p2)
        # script, div = components( gridplot([ fig_list ]) )
        plots.append((machine + ' Last weak scaling on up to > 512 nodes :' + df_filtered.iloc[0]['date'] , div, script))

        #################################################################################
        ### Third part: for a given test, give performance history for several n_node ###
        #################################################################################
        # Which quantities to plot on this dataframe
        x_axis = 'date'
        y_axis = 'step_time' 
        x_label = x_axis
        y_label = y_axis + ' (s)'
        # Prepare list of figures
        fig_list = []
        # Loop on n_node
        # One figure per value
        for count, n_node in enumerate( node_list ):
            df_filtered = df[ df['n_node']==n_node ]
            y_data_allmax = df_filtered[y_axis].max()
            fig = figure(width=250, plot_height=250, title='n_node = ' + str(n_node), 
                         x_axis_type="datetime", y_axis_type='log')
            # y_range=[0., 1.1*y_data_allmax], 
            # Ugly trick to have the legend outside the plot.
            # The last plot of the line is larger, and a fraction of 
            # it contains the legend...
            if count==len( node_list ) - 1:
                fig = figure(width=440, plot_height=250, title='n_node = ' + str(n_node), 
                             x_axis_type="datetime", y_axis_type='log')
            # y_range=[0., 1.1*y_data_allmax], 
            # Loop in put_file, i.e. different tests,
            # Shown on the same figure with different colors
            legend_it = []
            for inner_count, input_file in enumerate( df_filtered['input_file'].unique() ):
                color = color_list[inner_count]
                x_data = pd.to_datetime(df_filtered[df_filtered['input_file']==input_file][x_axis])
                y_data = df_filtered[df_filtered['input_file']==input_file][y_axis]
                c = fig.circle(x_data, y_data, size=5, fill_color=color, line_color=color, 
                           alpha=.5)
                legend_it.append((input_file.replace('automated_test_',''), [c]))
            fig.xaxis.axis_label = x_label
            fig.yaxis.axis_label = y_label
            fig_list.append( fig )
        # For the legend ugly trick
        legend = Legend(items=legend_it, location=(0, 0))
        legend.click_policy="mute"
        fig.add_layout(legend, 'right')
        # Store each plot in a 2d, here we chose a single row 
        p3 = gridplot([ fig_list ])
        div, script = components(p3)
        # script, div = components( gridplot([ fig_list ]) )
        print(machine + ' Performance history for each number of node')
        plots.append((machine + ' Performance history for each number of node', div, script))

        f.write(template.render(L=plots))
