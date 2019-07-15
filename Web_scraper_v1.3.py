# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 04:22:25 2019

@author: Manu Srivastava
"""

''' Tool to scrape websites'''

import requests
import csv
from bs4 import BeautifulSoup
WEBSITE = 'https://www.fullcompass.com'

def write_csv(brand, model_name, availability = '0',price = '',product_id = '',subcategory = '', large_images = '',short_description = '',mid_description = '',large_description = ''):
    row = [brand, model_name, availability,price,product_id,subcategory,large_images[0],short_description,mid_description,large_description]
    try:
        f = open('full_compass_products.csv', 'a', newline='',encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(row)
        for i in range(1,len(large_images)):
            writer.writerow([brand,model_name, '', '', '', '', large_images[i], '', '', ''])
        f.close()
    except:
        print('File write error')
        f.close()

def traverse_items(sauce):
    subcategory = sauce.h1.string
    while True:
       for data in sauce.select(".prod"):
           brand = title = model_name = price = product_id = short_description = availability = large_description = ''
           large_images = mid_description = []
           try:
               #print(data)
               brand = data['brand']
               title = data['product_name']
               model_name = title.replace(str(brand) + ' ', '', 1)
               price = data['price']
               product_id = data['product_id']
               #thumbnail = data.img['src']
               short_description = data.find(class_='short-description').string
               if data.find(class_='availability').string == 'In Stock':
                   availability = 1
               print(title.strip(),price.strip())
               res = requests.get(data['href'])
               mint = BeautifulSoup(res.text, "html.parser")
               mid_description = mint.find(class_='shortDescription').get_text().strip().split('\n')
               large_images = []
               large_description = mint.find(itemprop='description')
               #Image roundup
               for img in mint.select('#productImage .mainProdImage a'):
                   large_images += [img['href']]
               #Write CSV
               #name, availability, price, product_id, thumbnail, images, short desc, mid description, large_description
               
           except Exception as e:
               print('----------ERROR------Individual information retreival error in ' + title)
               print(e)
           write_csv(brand, model_name,availability,price,product_id,subcategory,large_images,short_description,mid_description,large_description)
       nextlink = sauce.select(".prod-list-sort .sortBoxPageBottom *:last-child")
       try:
           req = requests.get(nextlink[0]['href'])
           sauce = BeautifulSoup(req.text, "html.parser")
       except KeyError:
           print('------------------------------------Reached end of sub-category----------------------------')
           break
       
#def traverse_items_breadth(sauce):
#    subcategory = sauce.h1.string
#    for data in sauce.select(".prod"):
#       brand = title = model_name = price = product_id = short_description = availability = large_description = ''
#       large_images = mid_description = []
#       try:
#           #print(data)
#           brand = data['brand']
#           title = data['product_name']
#           model_name = title.replace(str(brand) + ' ', '', 1)
#           price = data['price']
#           product_id = data['product_id']
#           #thumbnail = data.img['src']
#           short_description = data.find(class_='short-description').string
#           if data.find(class_='availability').string == 'In Stock':
#               availability = 1
#           print(title.strip(),price.strip())
#           res = requests.get(data['href'])
#           mint = BeautifulSoup(res.text, "html.parser")
#           mid_description = mint.find(class_='shortDescription').get_text().strip().split('\n')
#           large_images = []
#           large_description = mint.find(itemprop='description')
#           #Image roundup
#           for img in mint.select('#productImage .mainProdImage a'):
#               large_images += [img['href']]
#           #Write CSV
#           #name, availability, price, product_id, thumbnail, images, short desc, mid description, large_description
#           
#       except Exception as e:
#           print('----------ERROR------Individual information retreival error in ' + title)
#           print(e)
#       write_csv(brand, model_name,availability,price,product_id,subcategory,large_images,short_description,mid_description,large_description)
       
global_request = requests.get(WEBSITE)
global_soup = BeautifulSoup(global_request.text, "html.parser")

for global_items in global_soup.select("#shopList .padded .flyout >a"): 
   print('GLOBAL HEADINGS:', global_items['href']) #live-sound
   res = requests.get(global_items['href'])
   soup = BeautifulSoup(res.text, "html.parser")


   for items in soup.select(".categories a"):
       print('items:', items['href']) #microphones
    
       page = requests.get(WEBSITE + items['href']) #Attribute 'href' in items, a in bs4.element.string
       broth = BeautifulSoup(page.text,"html.parser")
       
       if len(broth.select(".categories a")) > 0:
           for links in broth.select(".categories a"):
               print('  ----', links['href']) #Dynamic microphones
               req = requests.get(WEBSITE + links['href'])
               sauce = BeautifulSoup(req.text,"html.parser")
#              nextlink = sauce.select(".prod-list-sort .sortBoxPageBottom *:last-child")
#              print(type(sauce))
#              while nextlink[0].get('href', False):
#               traverse_items_breadth(sauce)
               traverse_items(sauce)
       else:
           sauce = broth
#           traverse_items_breadth(sauce)
           traverse_items(sauce)
 
