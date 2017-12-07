# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:48:14 2017

@author: Speedy
"""

#-----------------------------------------------------------------------------
import os
# working directory
wd_folder = r"path/to/file"

# make sure in working directory
if os.getcwd() != wd_folder:
    print("\n[+] Working directory set to:\n\t {}\n".format(wd_folder) )
    os.chdir(wd_folder)
else:
    print("\n[+] Current working directory:\n\t {}\n".format(wd_folder) )

#-----------------------------------------------------------------------------


import datetime as dt
import random
import importlib as impl
import pandas as pd
import numpy as np
import talib as ta

from settings import API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
import histAPI
import func
import indicators as ind



#-----------------------------------------------------------------------------

# module loader
def relib():
        impl.reload(histAPI)
        impl.reload(func)
        impl.reload(ind)
        print("\n[+] Libraries loaded\n" )

relib()

#-----------------------------------------------------------------------------

#define storage location
#file_folder = r"C:\Users\Speedy\Desktop"
#file_name = "USD_JPY" + "_" + dateBegin +"_" + dateEnd + ".csv"


#-----------------------------------------------------------------------------

#define desired data
instrument = "USD_JPY"
dateBegin = "2017-11-28 13:00:00"
dateEnd = "2017-11-28 18:30:00"
granularity = "M5"


#-----------------------------------------------------------------------------
# Main program
#-----------------------------------------------------------------------------

# get data
dfprices = histAPI.getHistoricaldata( API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
                                   instrument, granularity, dateBegin,
                                   dateEnd ).get_data()

# split to Bid/Ask
dfdict = func.splitbidask(dfprices)


#-----------------------------------------------------------------------------
# indicators testing
#-----------------------------------------------------------------------------

dfbid = dfdict['bid']
dfbid.head()
dfbid.dtypes

df1 = ind.trix( dfbid, [10,15])
df1 = ind.sma( dfbid, window = [3,5,9])
df1 = ind.sma( dfbid, 'volume', [5])
df1 = ind.bband( dfbid, 21)

df1.head(30)

df1 = ( dfbid.pipe( ind.bband, 21)
                .pipe( ind.sma, [3,5,9])
                .pipe( ind.trix, [7,11])






#-----------------------------------------------------------------------------

# optimization for indicators
# find best correlation with shifted close

# apply indicators
#for k in list(dfdict.keys()):
#        dfdict[k] = ( dfdict[k].pipe( sma(dfdict))
#                                .pipe( FUNC( dfdict)
#
#                    )
#
#


#-----------------------------------------------------------------------------
# scratch pad
#-----------------------------------------------------------------------------





#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


#open file and check content
file_path = os.path.join(file_folder,file_name)

with open(os.path.normpath(file_path), "w+", ) as file_in:
    file_content = file_in.readlines()

# if empty write info and headers
if (len(file_content) == 0):
    print(" File is empty \n\n")

    # write data info
    file_in.write("Instrument:" + instrument + ",From:" + dateBegin +
                  ",To:" + dateEnd +"\n")

    # write column headers
    file_in.write("instrument, sampling, time, openBid, openAsk, highBid, highAsk, lowBid, lowAsk, closeBid, closeAsk, volume \n")


# if there is content, print first few lines
else:
    print("File content: \n", file_content[0:3])



#############################################################################
# !!!! DONT DELETE THIS !!!!
#############################################################################
# split the date range into chunks and loop through
random.seed(8)
hoursplit = 6
for dates in histAPI.daterange(dateBegin,dateEnd, hourchunk=hoursplit):

    # calculate chunk
    date1 = dates.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
    dateplusone = dates + dt.timedelta(hours=hoursplit)
    date2 = dateplusone.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
    print("-> ",  date1, " to ", date2, " <-  " )

    while(True):
        prices = histAPI.getHistoricaldata(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
                                   instrument, granularity, date1, date2 )
        err_resp = prices.get_data()

        print("[-] Any error:",err_resp, "\n\n")


        if(err_resp == 200):
            sleep_delay = random.randrange(0, 60, 10)
            time.sleep(sleep_delay)
            print("Sleep for {}".format(sleep_delay) )
            print("wake up")
            break

        if(err_resp == 204):
            break

        else:
            continue


file_in.close()
print("\n FINISH!!!")



