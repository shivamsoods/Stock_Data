import requests
from datetime import datetime
from datetime import timedelta  

from pytz import timezone
import time
import sys
import csv

def dayDiff(dh,dl):
	df=dh-dl
	if(df>0):
		df=1
	elif(df==0):
		df=0
	elif(df<0):
		df=-1	
	return df

def previousDayDiff(pdc, do):
	pdf=pdc-do
	if(pdf>0):
		pdf=1
	elif(pdf==0):
		pdf=0
	elif(pdf<0):
		pdf=-1	
	return pdf

def currentDayDiff(ltp, do):
	cdf=ltp-do
	if(cdf>0):
		cdf=1
	elif(cdf==0):
		cdf=0
	elif(cdf<0):
		cdf=-1	
	return cdf

def fiftyTwoWeek(ftl, pt):
	if(stockReturn>ftl and stockReturn<(ftl+.1*ftl)):
		stockReturn=1
	else:
		stockReturn=-1	
	return stockReturn

now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
now_server_time = now_asia - now_asia.replace(hour=18, minute=0) + timedelta(minutes=555) 
print(now_server_time)

with open('stock_data_tuesday.csv','r',newline='',encoding='utf-8-sig') as readFile:
	reader = csv.DictReader(readFile)
	# value = len(list(reader))

	for row in reader:
		dh=float(row["DH"])
		dl=float(row["DL"])
		pdc=float(row["PDC"])
		do=float(row["DO"])
		ltp=float(row["LTP"])
		com_name=str(row["NAME"])
		
		df=dayDiff(dh=dh,dl=dl)
		pdf=previousDayDiff(pdc=pdc,do=do)
		cdf=currentDayDiff(ltp=ltp,do=do)
		print(com_name+" ",df+pdf+cdf)
	 
	readFile.close()