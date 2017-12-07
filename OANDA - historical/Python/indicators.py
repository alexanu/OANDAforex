# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:22:59 2017

@author: Speedy
"""

import pandas as pd
import talib as ta
import datetime as dt
import func


# function to apply all technical indicators
def allTA(df):

        # time it
        tic = dt.datetime.now()

        # apply all indicators
        df = ( df.pipe(sma, 13)
                    .pipe( bband, [3,7,11])
                    .pipe(trix, [10,15])
                    )

        # print time taken
        tottime = (dt.datetime.now() - tic).total_seconds()
        print("\n[+] Indicators took {} seconds\n".format(tottime) )

        return True


# simple moving average
def sma(df, colm='close', window=[11]):

        if colm=='close':
            column = func.Cl(df)
            func_label = 'sma'

        if colm=='volume':
            column = func.Vol(df)
            func_label = 'volsma'

        # iterate through each window
        for wind in window:
            # create label
            label = func_label + str(wind)
            errlabel = label + 'err'
            # calc sma
            df[label] = ta.SMA( column, wind)
            df[errlabel] = df[label] - column


        return(df)


# Bollinger bands
def bband(df, window):
        # calc bollinger bands
        rowlist = list( ta.BBANDS( func.Cl(df), timeperiod=window))
        # convert to dataframe
        bands = pd.DataFrame( rowlist,
                     index=['bbandupper', 'bbandmid', 'bbandlower']).transpose()
        # merge result
        df = df.join(bands)
        return df


def trix(df, window=[11]):

        column = func.Cl(df)

        # iterate through each window
        for wind in window:
            # create labels
            label = 'trix' + str(wind)
            errlabel = label + 'err'
            # calc trix
            df[label] = ta.TEMA( column, wind)
            df[errlabel] = df[label] - 0

        return df


















