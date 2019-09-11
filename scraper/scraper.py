import requests
import numpy as np
import pandas as pd
import pymongo
import settings
import urllib3
from IPython.core.display import clear_output
from bs4 import BeautifulSoup

#connection = pymysql.connect(host='localhost', user='root', db='house', password='990274', charset='latin1', cursorclass=pymysql.cursors.DictCursor)
# from IPython.core.display import clear_output
# import numpy as np


url = "https://vancouver.craigslist.org/search/eby/hhh?hasPic=1"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


npo_houses = {}

house_no = 0

while True:

    response = requests.get(url, verify = False)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    houses = soup.find_all("p", {"class": "result-info"})

    bed_counts = []
    sqfts = []

    for house in houses:
        title = house.find('a', {'class': 'result-title'}).text
        location_tag = house.find('span', {'class': 'result-hood'})
        location = location_tag.text[2:-1] if location_tag else "N/A"
        date = house.find('time', {'class': 'result-date'}).text
        link = house.find('a', {'class': 'result-title'}).get('href')
        price = house.find('span', {'class': 'result-price'}).text.strip('$')
        house_response = requests.get(link)
        house_data = house_response.text
        house_soup = BeautifulSoup(house_data, 'html.parser')
        house_description_tag = house_soup.find('section', {'id': 'postingbody'})
        house_description = house_description_tag.text if house_description_tag else np.nan
        house_attributes_tag = house_soup.find('p', {'class': 'attrgroup'})
        house_attributes = house_attributes_tag.text if house_attributes_tag else np.nan
        house_no += 1

        if house.find('span', {'class': 'housing'}) is not None:
            if 'ft2' in house.find('span', {'class': 'housing'}).text.split()[0]:
                bed_count = np.nan
                bed_counts.append(bed_count)

                sqft = int(house.find('span', {'class': 'housing'}).text.split()[0][:-3])
                sqfts.append(sqft)

            elif len(house.find('span', {'class': 'housing'}).text.split()) > 2:
                bed_count = house.find('span', {'class': 'housing'}).text.replace("br", "").split()[0]
                bed_counts.append(bed_count)

                sqft = int(house.find('span', {'class': 'housing'}).text.split()[2][:-3])
                sqfts.append(sqft)

            elif len(house.find('span', {'class': 'housing'}).text.split()) == 2:
                bed_count = house.find('span', {'class': 'housing'}).text.replace("br", "").split()[0]
                bed_counts.append(bed_count)

                sqft = np.nan
                sqfts.append(sqft)

            else:
                bed_count = np.nan
                bed_counts.append(bed_count)

                sqft = np.nan
                sqfts.append(sqft)

        else:
            bed_count = np.nan
            bed_counts.append(bed_count)

            sqft = np.nan
            sqfts.append(sqft)


        npo_houses[house_no] = [title, location, date, link, price, bed_count, sqft, house_description]

 #       print('House Title:', title, '\nLocation:', location, '\nDate:', date, '\nLink:', link, '\nPrice:', price,
  #            '\nBed:', bed_count, '\nSqft:', sqft, '\nHouse Description:', house_description, '\n---')

    url_tag = soup.find('a', {'title': 'next page'})
    if url_tag.get('href'):
        url = 'https://vancouver.craigslist.org' + url_tag.get('href')
        print(url)
    else:
        break
print("Total Houses:", house_no)

npo_houses_df = pd.DataFrame.from_dict(npo_houses, orient='index',
                                       columns=['House Title', 'Location', 'Date', 'Link', 'Price', 'Bedrooms', 'Sqft',
                                                'House Description'])


npo_houses_df.to_csv('npo_houses.csv')