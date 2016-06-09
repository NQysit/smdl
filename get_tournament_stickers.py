# -*- coding: utf-8 -*-

# SMDL
# Steam Market DownLoader
# v 0.1
# 5/6/2016
# NQysit

import os
import time
import pprint
import requests
from bs4 import BeautifulSoup

# tournaments IDs
# 1 - 2013 DreamHack Winter
# 3 - 2014 EMS One Katowice
# 4 - 2014 ESL One Cologne
# 5 - 2014 DreamHack Winter
# 6 - 2015 ESL One Katowice
# 7 - 2015 ESL One Cologne
# 8 - 2015 DreamHack Cluj-Napoca
# 9 - 2016 MLG Columbus

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
url_json = ('http://steamcommunity.com/market/search/render/'
            '?category_730_Tournament[0]=tag_Tournament{id_tournament}'
            '&category_730_Type[0]=tag_CSGO_Tool_Sticker&appid=730').format(id_tournament=id_tournament)

r = requests.get(url_json)
total_count = r.json()['total_count']

items_per_page = 10
total_pages = int(total_count / items_per_page) + 1

url = ('http://steamcommunity.com/market/search/'
       '?category_730_Tournament[0]=tag_Tournament{id_tournament}'
       '&category_730_Type[0]=tag_CSGO_Tool_Sticker&appid=730'
       '&start={start_at}'
       '&count={items_per_page}'
       '&sort_column=name&sort_dir=asc')

if not os.path.exists('stickers'):
    os.mkdir('stickers')

for n_page in range(total_pages):

    market_urls = []
    names = []
    img_urls = []

    rq = requests.get(url.format(id_tournament=id_tournament, start_at=n_page * items_per_page, items_per_page=items_per_page))
    soup = BeautifulSoup(rq.text, 'html.parser')

    for tag in soup.find_all('span', 'market_listing_item_name'):
        names.append(tag.text)

    for link in soup.find_all('a', 'market_listing_row_link'):
        market_urls.append(link['href'])

    for img in soup.find_all('img', 'market_listing_item_img'):
        img_urls.append(img['src'].replace('/62fx62f', '/94fx94f'))

    stickers = {}

    for market_url, name, img_url in zip(market_urls, names, img_urls):

        print('Downloading ', name.split('|')[1].strip())

        if name not in stickers:

            path = 'stickers/{name}.png'.format(name=name.split('|')[1].strip())

            stickers[name] = {
                'market_url': market_url,
                'img_url': img_url
            }

            if not os.path.isfile(path):
                rq = requests.get(img_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
                })
                open(path, mode='wb').write(rq.content)

            time.sleep(5)

open('stickers.py', mode='wt').write('stickers = ' + pprint.pformat(stickers))

