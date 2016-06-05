# -*- coding: utf-8 -*-

# SMDL
# Steam Market DownLoader
# v 0.1
# 5/6/2016
# NQysit

import time
import json
import pprint
import requests
import urllib
import json
import pprint
import wget
from bs4 import BeautifulSoup 

#tournaments IDs
#1 - 2013 DreamHack Winter
#3 - 2014 EMS One Katowice
#4 - 2014 ESL One Cologne
#5 - 2014 DreamHack Winter
#6 - 2015 ESL One Katowice
#7 - 2015 ESL One Cologne
#8 - 2015 DreamHack Cluj-Napoca
#9 - 2016 MLG Columbus
tournaments = [
    '',
    '2013 DreamHack Winter',
    '',
    '2014 EMS One Katowice',
    '2014 ESL One Cologne',
    '2014 DreamHack Winter',
    '2015 ESL One Katowice',
    '2015 ESL One Cologne',
    '2015 DreamHack Cluj-Napoca',
    '2016 MLG Columbus'
]
id_tournament = 3

url_json = 'http://steamcommunity.com/market/search/render/?category_730_Tournament[0]=tag_Tournament' + str(id_tournament) + '&category_730_Type[0]=tag_CSGO_Tool_Sticker&appid=730'

#get total items for current tournament from json
print('Getting total items...')

r = requests.get(url_json)
total_count = r.json()['total_count']

#get steam market urls
print('Composing market URLs...')

urls = []
items_per_page = 10
max_for = (int(total_count / items_per_page) + 1)
for i in range(0, max_for):
    u = 'http://steamcommunity.com/market/search/'
    u = u + '?category_730_Tournament[0]=tag_Tournament' + str(id_tournament)
    u = u + '&category_730_Type[0]=tag_CSGO_Tool_Sticker&appid=730'
    u = u + '&start=' + str(i * items_per_page) 
    u = u + '&count=' + str(items_per_page)
    u = u + '&sort_column=name&sort_dir=asc'
    urls.append(u)

#parse urls
print('Parsing URLs...')

market_urls = []
names = []
imgs_urls = []

for url in urls:
    
    #wait 1 second for antiddos
    time.sleep(1)
    
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, "html5lib")
    
    for tag in soup.find_all('span', 'market_listing_item_name'):
        names.append(tag.text)
            
    for link in soup.find_all('a', 'market_listing_row_link'):
        market_urls.append(link['href'])
        
    for img in soup.find_all('img', 'market_listing_item_img'):
        imgs_urls.append(img['src'].replace('/62fx62f','/94fx94f'))


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
}    

#Download images and generate json
stickers = {}
cont = 1
for market_url, name, img_url in zip(market_urls, names, imgs_urls):
        
    if name not in stickers:

        #stickers[name] = {'market_hash_name' : market_url, 'icon_url' : img_url}
        stickers[name] = {'market_url' : market_url, 'img_url' : img_url}
            
        print('Downloading ' + str(cont) + '/' + str(total_count) + "...")
        wget.download(img_url, './stickers/' + name + '.png')
        print(' ')
        
        #wait 5 seconds for antiddos
        time.sleep(5)
        
    cont = cont + 1

open('stickers.py', mode='wt').write('stickers = ' + pprint.pformat(stickers))

