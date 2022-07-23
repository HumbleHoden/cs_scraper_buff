import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import re
import array
from typing import Pattern
import random
pattern = r'\\*u\d{4}'
pattern2 = r' *'
localtime = time.localtime()
print(localtime)
 
def mergesort(a):
    def perform_merge(a, start, mid, end):
        # Merges two previously sorted arrays
        # a[start:mid] and a[mid:end]
        tmp = []
        for i in a:
            tmp.append(i)
        def compare(tmp, i, j):
            if profitability(tmp[i]) >= profitability(tmp[j]):
                i += 1
                return tmp[i-1]
            else:
                j += 1
                return tmp[j-1]
        i = start
        j = mid + 1
        curr = start
        while i<=mid or j<=end:
            if i<=mid and j<=end:
                if profitability(tmp[i]) >= profitability(tmp[j]):
                    a[curr] = tmp[i]
                    i += 1
                else:
                    a[curr] = tmp[j]
                    j += 1
            elif i==mid+1 and j<=end:
                a[curr] = tmp[j]
                j += 1
            elif j == end+1 and i<=mid:
                a[curr] = tmp[i]
                i += 1
            elif i > mid and j > end:
                break
            curr += 1
 
 
    def mergesort_helper(a, start, end):
        # Divides the array into two parts
        # recursively and merges the subarrays
        # in a bottom up fashion, sorting them
        # via Divide and Conquer
        if start < end:
            mergesort_helper(a, start, (end + start)//2)
            mergesort_helper(a, (end + start)//2 + 1, end)
            perform_merge(a, start, (start + end)//2, end)
 
 
    # Sorts the array using mergesort_helper
    mergesort_helper(a, 0, len(a)-1)
    

"""#for using selenium
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
driver = webdriver.Firefox(executable_path=r'D:/programming/selenium/Drivers/geckodriver')
firefox_service = Service(driver)
"""

#cookie settings
def cookiestring_to_cookies(cookiestring = ''):
    cookiesarray = []
    cookiestring = cookiestring.split('; ')
    for i in cookiestring:
        cookiesarray.append(i.split('=')[1])

    Device_Id       = cookiesarray[0]
    P_INFO          = cookiesarray[1]
    remember_me     = cookiesarray[2]
    session         = cookiesarray[3]
    Locale_Supported= cookiesarray[4]
    game            = cookiesarray[5]
    csrf_token      = cookiesarray[6]
    #_ga             = ""
    #_gid            = ""
    NTES_YD_SESS    = ""
    S_INFO          = ""

    cookies = {'Device-Id': Device_Id
                ,'Locale-Supported':Locale_Supported
                ,'game':game
                ,'NTES_YD_SESS':NTES_YD_SESS
                ,'S_INFO':S_INFO
                ,'P_INFO':P_INFO
                ,'remember_me':remember_me
                ,'session':session
                ,'csrf_token':csrf_token}#,'ga':_ga,'_gid':_gid
    return cookies

"""
driver.manage().addCookie('Device-Id', Device_Id)
driver.manage().addCookie('Locale-Supported',Locale_Supported)
driver.manage().addCookie('game',game)
driver.manage().addCookie('NTES_YD_SESS',NTES_YD_SESS)
driver.manage().addCookie('S_INFO',S_INFO)
driver.manage().addCookie('P_INFO',P_INFO)
driver.manage().addCookie('remember_me',remember_me)
driver.manage().addCookie('session',session)
driver.manage().addCookie('csrf_token',csrf_token)
"""

default_buff_address = 'https://buff.163.com'
marketapi = '/api/market/goods?game=csgo&page_num='
market = '/market/csgo#tab=selling&page_num='
order = '&min_price=30&sort_by=price.asc'
goods = '/goods/'
sellingpage = '?from=market#tab=selling'
buyorderpage = '?from=market#tab=buying'
recordpage = '?from=market#tab=history'

def buff_weaponsite(item_id,option = 'sellingpage'):
    if 'buy' in option:
        return default_buff_address + goods + str(item_id) + buyorderpage
    elif 'record' in option:
        return default_buff_address + goods + str(item_id) + recordpage
    else:
        return default_buff_address + goods + str(item_id) + sellingpage



def buff_marketapi_url(page_num):
    return default_buff_address + marketapi + str(page_num) + order
def buff_market_url(page_num):
    return default_buff_address + market + str(page_num) + order
#url looks like this   https://buff.163.com/api/market/goods?game=csgo&page_num=1&min_price=1000&sort_by=price.asc

apiurl = buff_marketapi_url(1)
url    = buff_market_url(1)
#driver.get(url)
#html_text = requests.get(url, cookies=cookies)
#soup = BeautifulSoup(html_text.content,'lxml')


class cs_item:
    def __init__(self,buy_order_prize,buyorders,steamprice_cny,id,name,quicksell_price,listed_prize,listed_quantity,fees = 0.025):
        self.name               = name
        self.buy_order_prize    = buy_order_prize
        self.buyorders          = buyorders
        self.listed_prize       = listed_prize
        self.listed_quantity    = listed_quantity
        self.steamprice_cny     = steamprice_cny
        self.id                 = id
        self.quicksell_price    = quicksell_price
        self.fees               = fees

def profitability(self):
    if (float(self.buy_order_prize)) != 0 : return float((float(self.quicksell_price) * (1-float(self.fees)))/(float(self.buy_order_prize)*1.02)-1)
    else: return float(0)


def print_item(self):
    print("The Item " + self.name + " has a profitabiltity of " + str(100 * profitability(self)) + "%" + " and " + str(self.listed_quantity) + " are currently selling\n")

def extract_items(page_num,itemarray,cookies):
    apiurl = buff_marketapi_url(page_num)
    api_text = requests.get(apiurl, cookies=cookies)
    apisoup = BeautifulSoup(api_text.content,'lxml')
    itemlist = apisoup.text.translate({ord(letter): None for letter in '"}{][\n\\'}).split(',')
    itemaccu = 0
    for line in itemlist:
        if 'buy_max_price:' in line:
            buy_max_price = float(re.sub(pattern2, '', line.split(':')[1]))
            itemaccu = 1
        elif 'buy_num:' in line:
            buy_num = int(re.sub(pattern2, '', line.split(':')[1]))
            itemaccu += 1
        elif "steam_price_cny:" in line:
            steam_price_cny = float(re.sub(pattern2, '', line.split(':')[1]))
        elif (itemaccu == 2) & ('id:' in line) & ('item_id' not in line):
            id = (re.sub(pattern2, '', line.split(':')[1]))
            itemaccu += 1
        elif "market_hash_name:" in line:
            name = (re.sub(pattern, '', line.split(':')[1]))
        elif "quick_price:" in line:
            quick_price = float(re.sub(pattern2, '', line.split(':')[1]))
        elif "sell_min_price:" in line:
            sell_min_price = float(re.sub(pattern2, '', line.split(':')[1]))
        elif "sell_num:" in line:
            sell_num = int(re.sub(pattern2, '', line.split(':')[1]))
            item = cs_item(buy_max_price
                                        ,buy_num
                                        ,steam_price_cny
                                        ,id
                                        ,name
                                        ,quick_price
                                        ,sell_min_price
                                        ,sell_num)
            if ('Graffiti' not in name) and ('Souvenir' not in name) and ('Sticker' not in name):
                if (sell_num >=7) and (buy_num >= 5) and (buy_max_price <= 1000):
                    itemarray.append(item)
                    print(name)

buff_cookiesstring = input("Enter cookiestring:")
if len(buff_cookiesstring) < 15:
    buff_cookies = cookiestring_to_cookies()
else: buff_cookies = cookiestring_to_cookies(buff_cookiesstring)
itemarray = []
for i in range(150):
    extract_items(i,itemarray,buff_cookies)
    print(str(i) + '\n')
    time.sleep(random.uniform(4,6))

mergesort(itemarray)
with open ('ab_30y.txt','w') as f:
    for i in itemarray:
        f.write("The Item " + i.name + " has a profitabiltity of " + str(100 * profitability(i)) + "%" + " and " + str(i.listed_quantity) + " are currently selling\n")
localtime = time.localtime()
print(localtime)
