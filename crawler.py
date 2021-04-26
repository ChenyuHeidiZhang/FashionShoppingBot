# Crawl information from clothing websites and store in csv file
# columns: id, title (& description), image url, original website link, brand, price, 
# text representation, image representation

import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
import os
import time

import encoder

class Site():
    def __init__(self, link):
        self.link = link

def get_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def parse_item(url):
    print(url)
    time.sleep(10)
    soup = get_soup(url)
    img = soup.find("div", class_="c-pwa-image-viewer__img-outer")
    img_url = img.find("picture").find("img").get("src")
    desc = soup.find("h1", class_="c-pwa-product-meta-heading").text.strip()
    price = soup.find("p", class_="c-pwa-product-price").find("span").text.strip()
    color = soup.find("span", class_="c-pwa-sku-selection__color-value").text.strip()
    return {
        'descrption': desc,
        'img_url': img_url,
        'url': url,
        'brand': "urban outfitter",
        'price': price,
        'color': color,
        'text_repr': encoder.encode_text(desc),
        'img_repr': encoder.encode_img(img_url)
    }

def crawl(df, site, csv_file):
    soup = get_soup(site)
    num_pages = int(soup.find("ul", class_="o-pwa-pagination").find_all("li")[1] \
        .find("a").get("aria-label").split()[-1])
    print("Number of pages in total:", num_pages)

    for page in range(1, num_pages+1):
        print("Currently on page", page)
        page_i = site + "?page={}".format(str(page))
        soup = get_soup(page_i)
        for tile in soup.find_all("div", class_="c-pwa-product-tile"):
            link = tile.find("a", recursive=False)
            href = urllib.parse.urljoin(site, link.get("href"))
            try:
                row = parse_item(href)
                #df = df.append(row, ignore_index=True)
            except urllib.error.HTTPError:
                print("HTTP Error")
            break
        break

    return df


if __name__ == "__main__":
    csv_file = "items.csv"

    if not os.path.exists(csv_file):
        column_names = ['descrption', 'img_url', 'url', 'brand', 'price', 'color', 'text_repr', 'img_repr']
        df = pd.DataFrame(columns = column_names)
        df.to_csv(csv_file, index=True)
    else:
        df = pd.read_csv(csv_file, index_col=0)
        print(df)
    site = "https://www.urbanoutfitters.com/"
    women = True
    if women:
        site += "womens-clothing"
    else:
        site += "mens-clothing"
    df = crawl(df, site)
    df.index.name = "id"
    print(df)

    df.to_csv(csv_file, index=True)
