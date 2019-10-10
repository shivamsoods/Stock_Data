from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
from datetime import datetime
from pytz import timezone
import time
import sys
import pymongo

format = "%Y-%m-%d %H:%M:%S"
format_date = "%Y-%m-%d"
format_hour = "%H"
format_min = "%M"
uri = "mongodb://shivamkapila:shivam123@ds333238.mlab.com:33238/stocks"
link_text='https://secure.icicidirect.com/IDirectTrading/Trading/trading_stock_quote.aspx?Symbol='
soup=BeautifulSoup

data=pd.read_csv('Nifty_50_list.csv')
com_code=data[['CODE']]

while(1):
    client = pymongo.MongoClient(uri)

    db = client.get_default_database()

    stock_data = db['stock_data']

    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))

    check9am = now_asia.replace(hour=17, minute=7)
    check3pm = now_asia.replace(hour=17, minute=12)
    if(now_asia > check9am and now_asia < check3pm):
        arr = []
    
        for i in range(0,50):
            site_html=requests.get(link_text+com_code["CODE"][i])
            bs4_html = BeautifulSoup(site_html.content, 'html5lib') 
            
            table1=bs4_html.find('table',class_='smallfont1')
            t2=table1.find('tbody')
            data_row=t2.find_all('tr')

            ltp=data_row[1].find_all('td')[1].text.strip()
            dc=data_row[2].find_all('td')[1].text.strip()
            do=data_row[3].find_all('td')[1].text.strip()
            dh=data_row[4].find_all('td')[1].text.strip()
            dl=data_row[5].find_all('td')[1].text.strip()
            pdc=data_row[6].find_all('td')[1].text.strip()
            date_time=now_asia.strftime(format)
            date_today=now_asia.strftime(format_date)
            hour=now_asia.strftime(format_hour)
            min=now_asia.strftime(format_min)
            cur_data = {
                'code': com_code["CODE"][i],
                'ltp': ltp,
                'dc': dc,
                'do': do,
                'dh': dh,
                'dl': dl,
                'pdc': pdc,
                'date_time': date_time,
                'date_today': date_today,
                'hour': hour,
                'min': min             
                }
            arr.append(cur_data)
            print(com_code["CODE"][i],ltp,dc,do,dh,dl,pdc,date_time,date_today,hour,min)
        print(arr)
        stock_data.insert_many(arr)
                
        time.sleep(30)

