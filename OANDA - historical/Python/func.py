# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 14:06:35 2017

@author: Amir Azmi
"""

#----------------------------------------------------------------------------
import re

#----------------------------------------------------------------------------

# function to split bid/ask
def splitbidask(df):
    # create filters to split bid/ask
    col_names = list( df.columns.values)
    bid_colm = (["time"] + list( filter( re.compile(".*Bid").match, col_names)) +
                    ["volume"])
    ask_colm = (["time"] + list( filter( re.compile(".*Ask").match, col_names)) +
                    ["volume"])
    # separate
    dfbid = df.loc[:, bid_colm]
    dfask = df.loc[:, ask_colm]

    # apply column names
    colm_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    dfbid.columns = colm_names
    dfask.columns = colm_names

    return { 'bid': dfbid, 'ask': dfask}


# function to get close values
def Cl(df):
        return df['close'].values


# function to get open values
def Op(df):
        return df['open'].values


# function to get high values
def Hi(df):
        return df['high'].values


# function to get low values
def Lo(df):
        return df['low'].values


# function to get volume values
def Vol(df):
        return df['volume'].values




