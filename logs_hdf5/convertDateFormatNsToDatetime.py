#! /usr/bin/env python

import pandas as pd
import sys

# Read hdf5 file with pandas format
perf_database_file = sys.argv[1]
df = pd.read_hdf( perf_database_file )

# Deep copy to new dataframe
df_new = df.copy()
# Reformat dates in df_new 
for i in range(df.shape[0]):
    if '-' not in str(df.loc[i,'date']):
        df_new.loc[i,'date'] = pd.to_datetime( df.loc[i,'date'] )

# Write new dataframe to file
df_new.to_hdf('NEW_' + perf_database_file, key='all_data', mode='w')
