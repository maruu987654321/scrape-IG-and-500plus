import pandas as pd
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import csv

buy = []
sell = []
res_instr = []
seller = []
buyers = []

def get_link():
    link = []
    instrument = pd.read_csv('name_500.txt')  
    f_res = []
    with open('name_all.txt', 'r') as fileobj:       
        for row in fileobj:
            f_res.append( row.rstrip('\n') )

    instrument_df = instrument[instrument['INSTRUMENTAL'].isin(f_res)]
    if len(instrument_df) != 0:
        instrument_lst = instrument_df['RES_INSTRUMENTAL'].tolist()
        for i in instrument_lst:
            res_instr.append(i)
            link.append('https://www.plus500.com/Instruments/{}'.format(i))
    
    return link

def parse_url(link, res_instr):
    date = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    for l in link:
        date.append(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        url = l
        main_info = requests.get(url, headers=headers).text
        soup = BeautifulSoup(main_info, 'lxml')
        all_scripts = soup.find_all('script')
        str_res = all_scripts[9]
        str_res = str(all_scripts[9])
        n = str_res.split('instruemntId')[1]
        for item in n.split('arrowDirection')[0].split(':'):
            vlue = item.split('\r')
            try:
                if 'SellPrice' in vlue[1]:
                    a = vlue[0].replace(',', '')
                    a = a.rstrip()
                    a = a.lstrip()
                    a = a.replace("'","")
                    a = float(a)
                    buy.append(a)
                if 'HighPrice' in vlue[1]:
                    b = vlue[0].replace(',', '')
                    b = b.rstrip()
                    b = b.lstrip()
                    b = b.replace("'","")
                    b = float(b)
                    sell.append(b)
            except IndexError :
                continue
        for item in n.split('arrowDirection')[0].split(':'):
            vlue2 = item.split('\r')
            try:
                if 'UsersBuyPercentage' in vlue2[1]:
                    a = vlue2[0].replace(',', '')
                    a = a.rstrip()
                    a = a.lstrip()
                    a = a.replace("'","")
                    a = int(a)
                    seller.append(a)
                if 'computed' in vlue2[4]:
                    b = vlue2[0].replace(',', '')
                    b = b.rstrip()
                    b = b.lstrip()
                    b = b.replace("'","")
                    b = int(b)
                    buyers.append(b)
            except IndexError :
                continue 
    return date, res_instr, sell, buy, buyers, seller

if __name__ == "__main__":
    link = get_link()
    result = parse_url(link, res_instr)
    try:
        with open("plus500.csv", "a") as f:
            w = csv.writer(f)
            for column in zip(*[s for s in result]):
                w.writerow(column)
    except IOError:
        with open('plus500.csv', 'w') as csvfile:
            csvw = csv.writer(csvfile, delimiter=',')
            for column in zip(*[s for s in result]):
                csvw.writerow(column)