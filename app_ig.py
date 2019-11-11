import pandas as pd
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def get_link():
    link = []
    commod = pd.read_csv('commod.txt')  
    forex = pd.read_csv('forex.txt') 
    indices = pd.read_csv('indices.txt') 
    f_res = []
    with open('name_all.txt', 'r') as fileobj:       
        for row in fileobj:
            f_res.append( row.rstrip('\n') )
    forex_df = forex[forex['FOREX'].isin(f_res)]
    commod_df = commod[commod['COMMOD'].isin(f_res)]
    indices_df = indices[indices['INDICES'].isin(f_res)]
    if len(forex_df) != 0:
        forex_lst = forex_df['RES_FOREX'].tolist()
        for i in forex_lst:
            link.append('https://www.ig.com/uk/forex/markets-forex/{}'.format(i))
    if len(commod_df) != 0:
        commod_lst = commod_df['RES_COMMOD'].tolist()
        for i in commod_lst:
            link.append('https://www.ig.com/uk/commodities/markets-commodities/{}'.format(i))
    if len(indices_df) != 0:
        indices_lst = indices_df['RES_INDICES'].tolist()
        for i in indices_lst:
            link.append('https://www.ig.com/uk/indices/markets-indices/{}'.format(i))
    return link

def parse_url(link):
    date = []
    bid = []
    ofr = []
    symbol = []
    cpt_2 = []
    cpc_2 = []
    price_ticket_percent = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    for item in link:
        main_info = requests.get(item, headers=headers).text
        soup = BeautifulSoup(main_info, 'lxml')
        cpt = soup.find_all("span", class_="price-ticket__change")[0].text.replace('pts', '')
        cpt = cpt.lstrip()
        cpt = cpt.rstrip()
        cpt_2.append(cpt)
        cpc = soup.find_all("span", class_="price-ticket__change")[1].text.replace('%', '')
        cpc = cpc.replace(')', '')
        cpc = cpc.replace('(', '')
        cpc = cpc.lstrip()
        cpc = cpc.rstrip()
        cpc_2.append(cpc)
        bid.append(soup.find_all("div", class_="price-ticket__price")[0].text)
        ofr.append(soup.find_all("div", class_="price-ticket__price")[1].text)   
        ticket = soup.find_all("div", class_="information-popup")[0].text
        ticket = ticket.replace('\r', '')
        ticket = ticket.replace('\n', '')
        new_ticket = ' '.join(ticket.split())
        price_ticket_percent.append(new_ticket.split('The')[0])
        symbol.append(item.split('/')[-1])
        date.append(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    return date, symbol, cpt_2, cpc_2, bid, ofr, price_ticket_percent
if __name__ == "__main__":
    lst_for_csv = []
    link = get_link()
    result = parse_url(link)
    try:
        with open("igindex.csv", "a") as f:
            w = csv.writer(f)
            for column in zip(*[s for s in result]):
                w.writerow(column)
    except IOError:
        with open('igindex.csv', 'w') as csvfile:
            csvw = csv.writer(csvfile, delimiter=',')
            for column in zip(*[s for s in result]):
                csvw.writerow(column)
    