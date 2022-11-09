# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: Garett Sidwell
Project: Data Quality Report
File name: data_quality_report.py
Date created: 09/02/2022
Date modified: 09/11/2022
Description: Quick data quality reports for both continuous and categorical data
'''

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

def dqr(df: pd.DataFrame, save_as_csv: bool = False) -> pd.DataFrame:
    '''Generates a basic Data Quality Report for the dataframe provided.

    Parameters
    ----------
    df: pd.DataFrame
      DataFrame containing the features and rows for the data that needs a Data Quality Report.
    save_as_csv: bool
      Boolean flag to indicate if you would like to save and export csv files containing the Data Quality Reports.

    Returns
    -------
    continuous_data: pd.DataFrame
      DataFrame contaiing the statistical summary and other data quality indicators (cardinality, missing values) for the continuous data
    
    categorical_data: pd.DataFrame
      DataFrame contaiing the statistical summary and other data quality indicators (cardinality, missing values) for the categorical data
    '''
    
    # Get data types
    data_types = pd.DataFrame(df.dtypes, columns=['data_type'])
    # Get count
    data_types['count']=df.count()
    # Calculate missing values as a percentage
    data_types['missing'] = round(((len(df)-df.count())/(len(df)))*100,2)
    # Determine cardinality
    card = [df[col].nunique() for col in df.columns]
    data_types['cardinality'] = card
    # Set features with a cardinality of 2 to categorical (because it is a bool)
    data_types['data_type'][data_types['cardinality'] == 2] = 'object'

    # Create Continuous and Categorical dataframes
    continuous_data = data_types[(data_types['data_type'] != 'object')|(data_types['data_type'] == 'datetime64[ns]')].copy()
    categorical_data = data_types[(data_types['data_type'] == 'object')&(data_types['data_type'] != 'datetime64[ns]')].copy()

    # Update Continuous Data Table
    continuous_data['min'] = [round(df[ind].min(),2) if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].min() for ind in continuous_data.index]
    continuous_data['1st qrt'] = [round(df[ind].quantile([.25]).values[0],2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].quantile([.25]).values[0] for ind in continuous_data.index]
    continuous_data['mean'] = [round(df[ind].mean(),2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].mean() for ind in continuous_data.index]
    continuous_data['median'] = [round(df[ind].median(),2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].median() for ind in continuous_data.index]
    continuous_data['3rd qrt'] = [round(df[ind].quantile([.75]).values[0],2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].quantile([.75]).values[0] for ind in continuous_data.index]
    continuous_data['max'] = [round(df[ind].max(),2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].max() for ind in continuous_data.index]
    continuous_data['std dev'] = [round(df[ind].std(),2)  if continuous_data.loc[ind,'data_type'] != '<M8[ns]' else df[ind].std() for ind in continuous_data.index]

    # Update Categorical Data Table
    mode = [df[ind].mode().values[0] for ind in categorical_data.index]
    mode_freq =[df[ind].value_counts().iloc[0] for ind in categorical_data.index]
    mode_perc = [round((mode_freq[i]/len(df)*100),2) for i in range(len(mode_freq))]
    mode_2 = [df[ind].value_counts().index[1] if categorical_data.loc[ind,'cardinality'] > 1 else np.nan for ind in categorical_data.index]
    mode_freq_2 = [df[ind].value_counts().iloc[1] if categorical_data.loc[ind,'cardinality'] > 1 else np.nan for ind in categorical_data.index ]
    mode_perc_2 = [round((mode_freq_2[i]/len(df)*100),2) for i in range(len(mode_freq_2))]


    categorical_data['mode'] = mode
    categorical_data['mode_freq'] = mode_freq
    categorical_data['mode_percent'] = mode_perc
    categorical_data['mode_2'] = mode_2
    categorical_data['mode_2_freq'] = mode_freq_2
    categorical_data['mode_2_perc'] = mode_perc_2

    continuous_data.sort_values('missing', ascending=False, inplace=True)
    categorical_data.sort_values('missing', ascending=False, inplace=True)

    if save_as_csv == True:
        continuous_data.to_csv(r'continuous_data.csv')
        categorical_data.to_csv(r'categorical_data.csv')

    return continuous_data, categorical_data
