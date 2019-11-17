import io
import shutil, os
from bokeh.plotting import figure, gridplot
from bokeh.models import Legend
from bokeh.embed import components
from jinja2 import Template
from bokeh.resources import INLINE
import pandas as pd
from bokeh.util.browser import view

dict_csv_files = {
    'Cori @ NERSC' : './logs_csv/cori_knl.csv',
    'Summit @ OLCF': './logs_csv/summit.csv'
    }

dict_hdf5_files = {
    'Cori @ NERSC' : './logs_hdf5/cori_results.h5',
    'Summit @ OLCF': './logs_hdf5/summit_results.h5'
    }

html_file = 'index.html'

# Convert hdf5 data to csv
for machine in list( dict_hdf5_files.keys() ):
    # Extract small data from data frame and write them to
    # First, generate csv files
    df = pd.read_hdf( dict_hdf5_files[machine] )
    # One large file
    df.loc[:,'step_time'] = pd.Series(df['time_running']/df['n_steps'], index=df.index)
    # Make smaller dataframe with only data to be written to csv file
    df_small = df.copy()
    df_small.loc[ df_small['input_file']=='automated_test_6_output_2ppc', 'step_time'] = \
        df_small[ df_small['input_file']=='automated_test_6_output_2ppc' ]['time_WritePlotFile']
    df_small = df_small.loc[:, ['date', 'input_file', 'git_hashes', 'n_node',
                                'n_mpi_per_node', 'n_omp', 'rep', 'start_date',
                                'time_initialization', 'step_time'] ]
    # Write to csv
    df_small.to_csv( dict_csv_files[machine] )
