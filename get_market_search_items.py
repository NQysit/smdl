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
            market_urls = []
            names = []
            img_urls = []
            
            path = os.path.join('stickers', query.replace(' ', '_'))
            if not os.path.exists(path):
                os.makedirs(path)

print('done!')
