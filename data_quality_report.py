# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
Author: Garett Sidwell
Project: Data Quality Report
File name: data_quality_report.py
Date created: 09/02/2022
Date modified: 09/02/2022
Description: Quick data quality reports for both continuous and categorical data
'''

import pandas as pd
import numpy as np

def dqr(df):
    '''
    This function genrates a basic Data Quality Report for the dataframe provided.
    The output is split into continuous and categorical features.
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
    continuous_data = data_types[data_types['data_type'] != 'object'].copy()
    categorical_data = data_types[data_types['data_type'] == 'object'].copy()

    # Update Continuous Data Table
    continuous_data['min'] = [round(df[ind].min(),2) for ind in continuous_data.index]
    continuous_data['1st qrt'] = [round(df[ind].quantile([.25]).values[0],2) for ind in continuous_data.index]
    continuous_data['mean'] = [round(df[ind].mean(),2) for ind in continuous_data.index]
    continuous_data['median'] = [round(df[ind].median(),2) for ind in continuous_data.index]
    continuous_data['3rd qrt'] = [round(df[ind].quantile([.75]).values[0],2) for ind in continuous_data.index]
    continuous_data['max'] = [round(df[ind].max(),2) for ind in continuous_data.index]
    continuous_data['std dev'] = [round(df[ind].std(),2) for ind in continuous_data.index]

    # Update Categorical Data Table
    mode_freq =[df[ind].value_counts()[0] for ind in categorical_data.index]
    mode_freq_2 =[df[ind].value_counts()[1] for ind in categorical_data.index]
    categorical_data['mode'] = [df[ind].mode().values[0] for ind in categorical_data.index]
    categorical_data['mode freq'] = mode_freq
    categorical_data['mode percent'] = [round((mode_freq[i]/len(df)*100),2) for i in range(len(categorical_data))]
    categorical_data['mode 2'] = [df[ind].value_counts().index[1] for ind in categorical_data.index]
    categorical_data['mode 2 freq'] = mode_freq_2
    categorical_data['mode 2 percent'] = [round((mode_freq_2[i]/len(df)*100),2) for i in range(len(categorical_data))]

    continuous_data.to_csv(r'continuous_data.csv')
    categorical_data.to_csv(r'categorical_data.csv')

    return continuous_data, categorical_data