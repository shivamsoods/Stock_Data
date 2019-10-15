import requests
from datetime import datetime
from datetime import timedelta
import json 
from flask import Flask, escape, request 
from pytz import timezone
import time
import sys
import csv

app = Flask(__name__)

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
def top_5():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M:%S"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('stock_data_tuesday1.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()

	per = []
	code = []
	inc = []
	with open('stock_data_tuesday1.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			dh=float(row["DH"])
			dl=float(row["DL"])
			pdc=float(row["PDC"])
			do=float(row["DO"])
			ltp=float(row["LTP"])
			com_name=str(row["NAME"])
			
			df=dayDiff(dh=dh,dl=dl)
			pdf=previousDayDiff(pdc=pdc,do=do)
			cdf=currentDayDiff(ltp=ltp,do=do)
			code.append(com_name)
			per.append(df+pdf+cdf) 
			inc.append((ltp - do)/ltp * 100)
			print(com_name, (ltp - do)/ltp * 100,df+pdf+cdf)
			
		readFile.close()

	for i in range(len(inc)):
		for j in range(i + 1, len(inc)):

			if inc[i] > inc[j]:
				inc[i], inc[j] = inc[j], inc[i]
				code[i], code[j] = code[j], code[i]
				per[i], per[j] = per[j], per[i]

	
	for i in range(len(per)):
		print(per[i],inc[i],code[i])

	count = 0
	codes = []

	for i in range(len(per)-1, -1, -1):
		if(per[i] == 3 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 2 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 1 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == 0 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	for i in range(len(per)-1, -1, -1):
		if(per[i] == -1 and count < 5):
			codes.append(code[i])
			count+=1
		if(count >4): 
			break
	print(codes)

	top_5_stocks = []
	for i in range(index+1,index+51):
		row = dict(reader[i])
		com_name=str(row["NAME"])
		for j in range(5):
			if(codes[j] ==com_name):
				top_5_stocks.append(row)

	return(top_5_stocks)


def search_stock(search_code):
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M:%S"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('stock_data_tuesday1.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
		index = i - 51
		readFile.close()
	with open('stock_data_tuesday1.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(index+1,index+51):
			row = dict(reader[i])
			com_name=str(row["NAME"])
			if(com_name == search_code):
				return(row)
			
		readFile.close()


def search_sensex():
	format = "%Y-%m-%d %H:%M:%S"
	format2 = "%H:%M:%S"
	now_utc = datetime.now(timezone('UTC'))
	now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
	now_server_time = now_asia - now_asia.replace(hour=0, minute=0) + timedelta(minutes=555) 
	diff2 = datetime.max

	with open('stock_data_tuesday1.csv','r',newline='',encoding='utf-8-sig') as readFile:
		reader = list(csv.DictReader(readFile))
		l = len(list(reader))
		for i in range(0,l,51):
			row = dict(reader[i])
			date_time=row["DATE_TIME"]
			dummydate = datetime.date(datetime.now())
			diff1 =  datetime.combine(dummydate,(datetime.min + now_server_time).time()) - datetime.combine(dummydate,(datetime.strptime(date_time,format)).time())
			if(diff1.total_seconds() < 0):
				break
			index = i - 51
		readFile.close()
		return(dict(reader[index]))



@app.route('/top5')
def top5():
    return json.dumps(top_5())

@app.route('/search')
def search():
 	search_code = request.args.get('code')
 	return json.dumps(search_stock(search_code))

@app.route('/sensex')
def sensex():
 	return json.dumps(search_sensex())

if __name__ == '__main__':
    app.run(debug=True)

