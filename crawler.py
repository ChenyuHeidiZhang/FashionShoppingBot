# Crawl information from clothing websites and store in csv file
# columns: id, title (& description), image url, original website link, brand, price, 
# text representation, image representation

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
import os

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

def crawl(df, site):
    soup = get_soup(site)
    for tile in soup.find_all("div", class_="c-pwa-product-tile"):
        link = tile.find("a", recursive=False)
        href = parse.urljoin(site, link.get("href"))
        row = parse_item(href)
        df = df.append(row, ignore_index=True)
        break
    return df


if __name__ == "__main__":
    csv_file = "items.csv"
    id = 0
    if not os.path.exists(csv_file):
        column_names = ['descrption', 'img_url', 'url', 'brand', 'price', 'color', 'text_repr', 'img_repr']
        df = pd.DataFrame(columns = column_names)
        df.to_csv(csv_file)
    else:
        df = pd.read_csv(csv_file)
    site = "https://www.urbanoutfitters.com/"
    women = True
    if women:
        site += "womens-clothing"
    else:
        site += "mens-clothing"
    df = crawl(df, site)
    df.index.name = "id"
    print(df)

    df.to_csv(csv_file)
