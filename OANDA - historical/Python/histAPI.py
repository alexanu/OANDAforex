# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 21:36:27 2016

@author: Amir Azmi
"""
#----------------------------------------------------------------------------

#" https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=2&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York"

# "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&start=2014-06-19T15%3A47%3A40Z&end=2014-06-19T15%3A47%3A50Z"


#----------------------------------------------------------------------------

import json
import requests
import datetime as dt
import pandas as pd

#----------------------------------------------------------------------------



class getHistoricaldata (object):

    def __init__(self, domain, access_token, account_id, instruments,
                 granularity, date1, date2):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.instruments = instruments
        self.granularity = granularity
        self.start = dt.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S"
                                          ).strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
        self.end = dt.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S"
                                        ).strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")


    def connect_to_server(self):
        try:
            print("\n -> Connecting to server..... ")
            s = requests.Session()
            url = ("https://" +
                   self.domain +
                   "/v1/candles?instrument=" +
                    self.instruments +
                    "&granularity=" +
                    self.granularity +
                    "&start=" +
                    self.start +
                    "&end=" +
                    self.end)
            print("\n -> URL:", url)
            headers = {"Authorization" : "Bearer " + self.access_token,
                       "Accept-Encoding": "gzip, deflate"}

#            Accept-Encoding: gzip, deflate


            req = requests.Request("GET", url, headers=headers)

            #, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=False, verify=True)

            print("\n\n --> Connection response code:", resp.status_code,"\n")
            print(" --> Response headers:")
            for k in resp.headers:
                print("\t", k,":", resp.headers[k])

            #view - test
#            print("URL: ", url)
#            print("HEADERS: ", headers)
#            print("PARAMS: ", params)

            return resp

        except Exception as e:
            s.close()
            print( "\n Caught exception when connecting to server \n\t " +
                      str(e) + "\n")



    def get_data(self):

            # add timer
            tic = dt.datetime.now()

            print("\n\n[+] +++ Fetching data +++ ")
            response = self.connect_to_server()

            #Response 204 if no data for the day
            if response.status_code != 200:
                if response.status_code == 204:
                    print("[+] No data for the requested period ")
                    err_response = response.status_code
                    return err_response
                else:
                    print(" !!! Connection Error. Server response code:",
                          response.status_code)
                    err_response = response.status_code
                    return err_response

            str_response = response.content.decode("utf-8")
            # see content
            #            print("texty: \n\n", str_response,
            #                  "\n\n end text \n\n")
            content = json.loads(str_response)

            instrument = content["instrument"]
            sampling = content["granularity"]
            print("\n\n[+] Instrument:", instrument,
                  "  Sampling:", sampling)

            # initialize dataframe
            df = pd.DataFrame( columns=["instrument", "sampling", "time",
                                         "openBid", "openAsk", "highBid",
                                         "highAsk", "lowBid", "lowAsk",
                                         "closeBid", "closeAsk", "volume"] )



            for count,i in enumerate(content["candles"]):
                if i["complete"]:
                    try:
                        time = i["time"][:-8]
                        openBid = i["openBid"]
                        openAsk = i["openAsk"]
                        highBid = i["highBid"]
                        highAsk = i["highAsk"]
                        lowBid = i["lowBid"]
                        lowAsk = i["lowAsk"]
                        closeBid = i["closeBid"]
                        closeAsk = i["closeAsk"]
                        volume = i["volume"]

                        content_list = [instrument, sampling, time, openBid,
                                        openAsk, highBid, highAsk, lowBid,
                                        lowAsk, closeBid, closeAsk, volume]
#                        print( content_list)

                        # previously: join as string
                        #content_str = ",".join(str(x) for x in content_list)

                        # combine into dataframe
                        df.loc[count,] = content_list

#                        print(content_str)

                    except Exception as e:
                         print("\n Error parsing data:" + str(e) + "\n")

            # set numeric type
            df = df.apply( pd.to_numeric, errors='ignore')
            # set datetime type
            df['time'] = pd.to_datetime( df['time'], format='%Y-%m-%d %H:%M:%S')
            df['volume'] = df['volume'].values.astype('float64')

#            print("\n\n END OF get_data \n\n")
            err_response = response.status_code

            getTime = (dt.datetime.now() - tic).total_seconds()
            print("\n[+] Get data took {} seconds\n".format(getTime) )

#            return err_response
            return(df)



# date range for iteration
def daterange(d1, d2, hourchunk=1):

    date1 = dt.datetime.strptime(d1,"%Y-%m-%d")
    date2 = dt.datetime.strptime(d2,"%Y-%m-%d")

    return [date1 + dt.timedelta(hours= hourchunk*i) for i in range( int(( (date2 - date1)/dt.timedelta(hours=hourchunk) ) ))]




