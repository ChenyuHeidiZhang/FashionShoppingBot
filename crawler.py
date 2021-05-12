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


def get_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


class Site():
    def __init__(self):
        self.link_female = ''
        self.link_male = ''

    def parse_item(self, url):
        raise NotImplementedError

    def crawl(self, csv_file):
        raise NotImplementedError

class Foreover21(Site):
    def __init__(self):
        link = "https://www.forever21.com/"
        self.link_female = link + "us/shop/catalog/category/f21/app-main"
        self.link_male = link + "us/shop/catalog/category/f21/mens-clothing"

    def parse_item(self, url):
        print(url)
        time.sleep(8)
        soup = get_soup(url)
        img_li = soup.find("li", class_="product-gallery__item slick-slide slick-current slick-active")
        img_url = img_li.find("button").find("img").get("src")
        desc = soup.find("h1", class_="pdp__name body-type--deka text-line--normal").text.strip()
        price = soup.find("span", class_="value price__default  font-weight--bold ").text.strip()
        color = soup.find("dive", class_="product-attribute product-attribute--color   ").find("div", class_="product-attribute__selected-value form-control-label ").find("span").text.strip()
        return {
            'descrption': desc,
            'img_url': img_url,
            'url': url,
            'brand': "forever 21",
            'price': price,
            'color': color,
            'text_repr': encoder.encode_text(desc),
            'img_repr': encoder.encode_img(img_url)
        }

    def crawl_female(self, csv_file):
        self.crawl(self.link_female, csv_file)
    def crawl_male(self, csv_file):
        self.crawl(self.link_male, csv_file)

    def crawl(self, site, csv_file):
        # 1-691: UO female
        # 692-1059: UO male
        # TODO: rework crawl to fit forever 21
        pass
        id = 1060  # 691 is the last female item
        with open(csv_file, 'a') as f:
            wr = csv.writer(f)
            soup = get_soup(site)
            num_pages = int(soup.find("div", class_="pagination__list flex flex-align-center flex-justify-center").find_all("button")[-2].text.strip())
            print("Number of pages in total:", num_pages)

            for page in range(num_pages):
                print("Currently on page", page+1)
                page_i = site + f"?start={page*32}&sz=32"
                soup = get_soup(page_i)
                for tile in soup.find_all("a", class_="product-tile__anchor product-tile__anchor--product-info"):
                    href = urllib.parse.urljoin(site, tile.get("href"))
                    try:
                        row = self.parse_item(href)
                        id += 1
                        row['id'] = id
                        wr.writerow([row[col] for col in column_names])
                    except urllib.error.HTTPError:
                        print("HTTP Error")
                    except KeyboardInterrupt:
                        return
                    except:
                        print("Some other error")

class Gap(Site):
    # TODO: fix cookie issues
    def __init__(self):
        link = "https://www.gap.com/"
        self.link_female = link + "browse/division.do?cid=5643"
        self.link_male = link + "browse/division.do?cid=5063"

    def parse_item(self, url):
        print(url)
        time.sleep(8)
        soup = get_soup(url)
        img = soup.find("a", class_="hover-zoom hover-zoom-in")
        img_url = img.get("href")
        desc = soup.find("h1", class_="pdp-mfe-ihsmt3").text.strip()
        price = soup.find("span", class_="pdp-pricing__selected ").text.strip()
        color = soup.find("span", class_="swatch-label__value").text.strip()
        return {
            'descrption': desc,
            'img_url': img_url,
            'url': url,
            'brand': "Gap",
            'price': price,
            'color': color,
            'text_repr': encoder.encode_text(desc),
            'img_repr': encoder.encode_img(img_url)
        }

    def crawl_female(self, csv_file):
        self.crawl(self.link_female, csv_file)
    def crawl_male(self, csv_file):
        self.crawl(self.link_male, csv_file)

    def crawl(self, site, csv_file):
        # 1-691: UO female
        # 692-1059: UO male
        id = 1060 
        with open(csv_file, 'a') as f:
            wr = csv.writer(f)
            
            soup = get_soup(site)
            categories = soup.find_all("div", class_="css-x66lwe")
            print(f"Number of categories: {len(categories)}")

            for category_root in categories:
                category = category_root.find("div", class_="css-1m4a7xd").find("div", class_="css-1bd70hp").find("a", class_="css-11pqejk")
                category_name = category.text.strip()
                category_link = urllib.parse.urljoin(site, category.get("href"))
                print(f"On category {category_name}")
                category_page = get_soup(category_link)
                # product grid: div class="product-card-grid__item-1-2 product-card-grid__item-lg-1-3 product-card-grid__item-xl-1-3 product-card-grid__item-1280-1-4"

                num_pages = int(category_page.find("div", class_="css-1f8u5hk").find_all("span")[1].text.strip())
                print(category_link)



            # for page in range(10, num_pages+1):
            #     print("Currently on page", page)
            #     page_i = site + "?page={}".format(str(page))
            #     soup = get_soup(page_i)
            #     #for tile in soup.find_all("div", class_="c-pwa-product-tile"):
            #     for tile in soup.find_all("div", class_="o-pwa-product-tile"):
            #         link = tile.find("a", recursive=False)
            #         href = urllib.parse.urljoin(site, link.get("href"))
            #         try:
            #             row = self.parse_item(href)
            #             id += 1
            #             row['id'] = id
            #             wr.writerow([row[col] for col in column_names])
            #         except urllib.error.HTTPError:
            #             print("HTTP Error")
            #         except KeyboardInterrupt:
            #             return
            #         except:
            #             print("Some other error")

class UO(Site):
    def __init__(self):
        link = "https://www.urbanoutfitters.com/"
        self.link_female = link + "womens-clothing"
        self.link_male = link + "mens-clothing"

    def parse_item(self, url):
        print(url)
        time.sleep(8)
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

    def crawl_female(self, csv_file):
        self.crawl(self.link_female, csv_file)
    def crawl_male(self, csv_file):
        self.crawl(self.link_male, csv_file)

    def crawl(self, site, csv_file):
        id = 1059  # 691 is the last female item
        with open(csv_file, 'a') as f:
            wr = csv.writer(f)

            soup = get_soup(site)
            num_pages = int(soup.find("ul", class_="o-pwa-pagination").find_all("li")[1] \
                .find("a").get("aria-label").split()[-1])
            print("Number of pages in total:", num_pages)

            for page in range(10, num_pages+1):
                print("Currently on page", page)
                page_i = site + "?page={}".format(str(page))
                soup = get_soup(page_i)
                #for tile in soup.find_all("div", class_="c-pwa-product-tile"):
                for tile in soup.find_all("div", class_="o-pwa-product-tile"):
                    link = tile.find("a", recursive=False)
                    href = urllib.parse.urljoin(site, link.get("href"))
                    try:
                        row = self.parse_item(href)
                        id += 1
                        row['id'] = id
                        wr.writerow([row[col] for col in column_names])
                    except urllib.error.HTTPError:
                        print("HTTP Error")
                    except KeyboardInterrupt:
                        return
                    except:
                        print("Some other error")

class Shein(Site):
    def __init__(self):
        link = "https://us.shein.com"
        self.link_female = link+"/Clothing-c-2035.html?ici=us_tab01navbar04&scici=navbar_WomenHomePage~~tab01navbar04~~4~~webLink~~~~0"
        self.link_male = link + "mens-clothing"

    def parse_item(self, url):
        print(url)
        #time.sleep(8)
        soup = get_soup(url)
        #img = soup.find("div", class_="swiper-slide product-intro__main-item cursor-zoom-in swiper-slide-active")
        img = soup.find("div", class_="goods-detailv2__media-inner")
        print(img)   # Can't find image div for some reason
        img_url = img.find("img").get("src")
        desc = soup.find("h1", class_="product-intro__head-name").text.strip()
        price = soup.find("div", class_="product-intro__head-price").find("div").find("div").get("aria-label")
        color = soup.find("span", class_="color-999").text.strip()
        return {
            'descrption': desc,
            'img_url': img_url,
            'url': url,
            'brand': "shein",
            'price': price,
            'color': color,
            'text_repr': encoder.encode_text(desc),
            'img_repr': encoder.encode_img(img_url)
        }

    def crawl_female(self, csv_file):
        self.crawl(self.link_female, csv_file)
    def crawl_male(self, csv_file):
        self.crawl(self.link_male, csv_file)

    def crawl(self, site, csv_file):
        id = 0
        with open(csv_file, 'a') as f:
            wr = csv.writer(f)

            print(site)
            soup = get_soup(site)
            #num_pages = int(soup.find("span", class_="S-pagination__total").text.split()[1])
            num_pages = 40
            print("Number of pages in total:", num_pages)

            for page in range(1, num_pages+1):
                print("Currently on page", page)
                page_i = site + "&page={}".format(str(page))
                soup = get_soup(page_i)
                for tile in soup.find_all("div", class_="S-product-item__wrapper"):
                    link = tile.find("a", recursive=False)
                    href = urllib.parse.urljoin(site, link.get("href"))
                    try:
                        row = self.parse_item(href)
                        id += 1
                        row['id'] = id
                        wr.writerow([row[col] for col in column_names])
                    except urllib.error.HTTPError:
                        print("HTTP Error")
                    # except KeyboardInterrupt:
                    #     return
                    # except:
                    #     print("Some other error")


# class Shein(Site):
#     def __init__(self):
#         link = "https://us.shein.com"
#         self.link_female = link+"/Clothing-c-2035.html?ici=us_tab01navbar04&scici=navbar_WomenHomePage~~tab01navbar04~~4~~webLink~~~~0"
#         self.link_male = link + "mens-clothing"

#     def parse_item(self, url):
#         print(url)
#         #time.sleep(8)
#         soup = get_soup(url)
#         #img = soup.find("div", class_="swiper-slide product-intro__main-item cursor-zoom-in swiper-slide-active")
#         img = soup.find("div", class_="goods-detailv2__media-inner")
#         print(img)   # Can't find image div for some reason
#         img_url = img.find("img").get("src")
#         desc = soup.find("h1", class_="product-intro__head-name").text.strip()
#         price = soup.find("div", class_="product-intro__head-price").find("div").find("div").get("aria-label")
#         color = soup.find("span", class_="color-999").text.strip()
#         return {
#             'descrption': desc,
#             'img_url': img_url,
#             'url': url,
#             'brand': "shein",
#             'price': price,
#             'color': color,
#             'text_repr': encoder.encode_text(desc),
#             'img_repr': encoder.encode_img(img_url)
#         }

#     def crawl_female(self, csv_file):
#         self.crawl(self.link_female, csv_file)
#     def crawl_male(self, csv_file):
#         self.crawl(self.link_male, csv_file)

#     def crawl(self, site, csv_file):
#         id = 0
#         with open(csv_file, 'a') as f:
#             wr = csv.writer(f)

#             print(site)
#             soup = get_soup(site)
#             #num_pages = int(soup.find("span", class_="S-pagination__total").text.split()[1])
#             num_pages = 40
#             print("Number of pages in total:", num_pages)

#             for page in range(1, num_pages+1):
#                 print("Currently on page", page)
#                 page_i = site + "&page={}".format(str(page))
#                 soup = get_soup(page_i)
#                 for tile in soup.find_all("div", class_="S-product-item__wrapper"):
#                     link = tile.find("a", recursive=False)
#                     href = urllib.parse.urljoin(site, link.get("href"))
#                     try:
#                         row = self.parse_item(href)
#                         id += 1
#                         row['id'] = id
#                         wr.writerow([row[col] for col in column_names])
#                     except urllib.error.HTTPError:
#                         print("HTTP Error")
#                     # except KeyboardInterrupt:
#                     #     return
#                     # except:
#                     #     print("Some other error")


def initialize_csv(csv_file, column_names):
    if not os.path.exists(csv_file):
        with open(csv_file, 'w') as f:
            wr = csv.writer(f)
            wr.writerow(column_names)


if __name__ == "__main__":
    csv_file = "items_0510.csv"
    column_names = ['id', 'descrption', 'img_url', 'url', 'brand', 'price', 'color', 'text_repr', 'img_repr']
    initialize_csv(csv_file, column_names)

    # site = UO()
    #site = Shein()
    # site = Gap()
    site = Foreover21()
    site.crawl_female(csv_file)

    df = pd.read_csv(csv_file, index_col=0)
    print(df.head())

