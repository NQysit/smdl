# -*- coding: utf-8 -*-

# SMDL
# Steam Market DownLoader
# v 0.2
# 12/6/2016
# NQysit

import sys
import os
import time
import pprint
import requests
from bs4 import BeautifulSoup

#extract script name from arguments
sys.argv.pop(0)

#get query
query = ''
for arg in sys.argv:
    query = query + ' ' + arg
query = query.strip()

if len(query) == 0:
    print('Enter some query!')
else:
    #get items
    start = 0
    count = 100
    total_count = 1
            
    market_urls = []
    names = []
    img_urls = []
    stickers = {}
    
    while(start < total_count):
        #wait 1 second for next json requests
        time.sleep(1)
        
        url_json = ('http://steamcommunity.com/market/search/render/'
                '?query={query}'
                '&start={start}'
                '&count={count}'
                '&sort_column=name&sort_dir=asc&appid=730'
        ).format(query=query,start=start,count=count)
        
        r = requests.get(url_json)
        total_count = r.json()['total_count']
        results_html = r.json()['results_html']
        start = start + count
        
        if total_count > 0:
            
            path = os.path.join('stickers', query.replace(' ', '_'))
            if not os.path.exists(path):
                os.makedirs(path)
            
            soup = BeautifulSoup(results_html, 'html.parser')

            for tag in soup.find_all('span', 'market_listing_item_name'):
                names.append(tag.text)
        
            for link in soup.find_all('a', 'market_listing_row_link'):
                market_urls.append(link['href'])
        
            for img in soup.find_all('img', 'market_listing_item_img'):
                img_urls.append(img['src'].replace('/62fx62f', '/94fx94f'))
                
            for market_url, name, img_url in zip(market_urls, names, img_urls):

                print('Downloading: ', name)
        
                if name not in stickers:
        
                    stickers[name] = {
                        'market_url': market_url,
                        'img_url': img_url
                    }
        
                    rq = requests.get(img_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
                    })
        
                    file_name = '{name}.png'.format(name=name)
        
                    open(os.path.join(path, file_name), mode='wb').write(rq.content)
        
                    time.sleep(2)
            
print('done!')
