from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone
import time
import sys
import pymongo
import csv

format = "%Y-%m-%d %H:%M:%S"
format_date = "%Y-%m-%d"
format_hour = "%H"
format_min = "%M"
uri = "mongodb://shivam:shivam123@ds333238.mlab.com:33238/stocks?retryWrites=false"
link_text='https://secure.icicidirect.com/IDirectTrading/Trading/trading_stock_quote.aspx?Symbol='
soup=BeautifulSoup

with open('stock_data_friday.csv','w',newline='',encoding='utf-8-sig') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow(['NAME','LTP','DC','DO','DH','DL','PDC','CH','PCH','DV','LTT','WH52','WL52','DATE_TIME','DATE_TODAY','HOUR','MIN'])
		writeFile.close()

com_code=['BSESEN','HDFBAN', 'RELPET', 'HDFC', 'INFTEC', 'ICIBAN', 'ITC', 'TCS', 'KOTMAH', 'LARTOU', 'HINLEV', 'AXIBAN', 'STABAN', 'BAJFI', 'MARUTI', 'INDBA', 'ASIPAI', 'BHAAIR', 'HCLTEC', 'TITIND', 'MAHMAH', 'BAFINS', 'NTPC', 'NESIND', 'POWGRI', 'ULTCEM', 'TECMAH', 'SUNPHA', 'ONGC', 'BAAUTO', 'BHARAS', 'INDOIL', 'COALIN', 'WIPRO', 'HERHON', 'BRIIND', 'UNIP', 'DRREDD', 'ADAPOR', 'GRASIM', 'VEDLIM', 'HINDAL', 'TATSTE', 'EICMOT', 'GAIL', 'JSWSTE', 'BHAINF', 'CIPLA', 'TATMOT', 'ZEEENT', 'YESBAN']
while(1):
    client = pymongo.MongoClient(uri)

    db = client.get_default_database()

    stock_data = db['stock_data_friday']

    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))

    check9am = now_asia.replace(hour=9, minute=15)
    check3pm = now_asia.replace(hour=15, minute=55)
    
    if(1):
        arr = []
    
        for i in range(0,50):
            site_html=requests.get(link_text+com_code[i])
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
            ch=data_row[7].find_all('td')[1].text.strip()
            pch=data_row[8].find_all('td')[1].text.strip()
            dv=data_row[11].find_all('td')[1].text.strip()
            ltt=data_row[2].find_all('td')[3].text.strip()
            wh52=data_row[7].find_all('td')[3].text.strip()
            wl52=data_row[8].find_all('td')[3].text.strip()


            date_time=now_asia.strftime(format)
            date_today=now_asia.strftime(format_date)
            hour=now_asia.strftime(format_hour)
            min=now_asia.strftime(format_min)
            cur_data = {
                'code': com_code[i],
                'ltp': ltp,
                'dc': dc,
                'do': do,
                'dh': dh,
                'dl': dl,
                'pdc': pdc,
                'ch': ch,
                'pch': pch,
                'dv': dv,
                'ltt': ltt,
                'wh52': wh52,
                'wl52': wl52,

                'date_time': date_time,
                'date_today': date_today,
                'hour': hour,
                'min': min             
                }
            arr.append(cur_data)
            # print(com_code[i],ltp,dc,do,dh,dl,pdc,date_time,date_today,hour,min)
            with open('stock_data_friday.csv','a',newline='',encoding='utf-8-sig') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([com_code[i],ltp,dc,do,dh,dl,pdc,ch,pch,dv,ltt,wh52,wl52,date_time,date_today,hour,min])
                writeFile.close()
        # print(arr)
        stock_data.insert_many(arr)      
        # time.sleep(1800)


