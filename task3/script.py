import requests
import csv
from lxml import html
import re
from datetime import datetime
from time import sleep
from random import randint
import random
import sys
import os

def get_data(page,user_agent, headers,cookies):  
    # makes requests for page data
    print("User Agent: ", user_agent)
    session = requests.Session()
    headers.update({'User-Agent':user_agent})
    try:
        assert page is not None
        response = session.get(
        f'https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260&page={page}'
        ,headers=headers,cookies=cookies)
        print("response status:", response.status_code)
        return response
    except requests.HTTPError as e:
        print("An http error has occured: ", e)
        sys.exit(e)
    except requests.ConnectionError as e:
        sys.exit(e)
    


def get_x_path_data(response): 
    #extract's desired data from reponse data using x_path
    if response.status_code == 200:
        
        tree = html.fromstring(response.content)
        assert tree is not None
        return tree.xpath("//body/script[5]/text()")[0]
    else:
        print("error occured: ", response.status_code)
        return 0

    


def extract_and_save_annonce(data:list, page:int, fields_dict:list,csv_writer): 
    #This function extracts annonce fields using a regex list and calls write_to_csv

    # Get all string structures that satisfy regex {list_id......has_phone: boolean}
    annonces = re.findall(
        r'{(\"list_id"\:[\W+\w+]*?\"has_phone"\:\w+)}', data)

    headers = [list(i.keys())[0] for i in fields_dict] #get headers
    headers.extend(['date_scraped','page_scraped'])
    fields = [list(i.values())[0] for i in fields_dict] #get fields
    rows = []
    for annonce in annonces:
        res = {}
        for field in fields:
            match = re.findall(field,annonce)
            title = headers[fields.index(field)]
            if len(match) > 0:
                if title == "Details": #can have Honoraires  or Reference or both
                    res.update({title: dict((x, y) for x, y in match)})
                else:
                    res.update(dict((title, y) for  y in match))
            else:
                if title == "Currency":
                    res.update({title:"EUR"})
                else:
                    res.update({title:"NULL"})
        
        date = datetime.today().strftime('%Y-%m-%d') #get current date
        res.update({'date_scraped': date})  # adds date_scraped to annonce
        res.update({'page_scraped': page})  # adds page_scraped to annonce
        rows.append(res)
        final_rows = isUnique(rows)
    csv_writer.write_to_csv(final_rows,page, headers)
#ensures that all data written to csv is unique

def isUnique(row:list):
   return  list({v['annonce_id']:v for v in row}.values())


class Csvwriter:
    def __init__(self, filename):
        self.filename = filename
    
    def write_to_csv(self, data: list, page: int, headers:list): 
        # This function writes the data to a csv filed
        file_exists = os.path.isfile(self.filename)
        with open('output.csv','a') as f:
            csv_writer = csv.DictWriter(f,fieldnames=headers)
            if not file_exists:
                csv_writer.writeheader()
            csv_writer.writerows(data)


# A list of regular expressions used to extract the target fields

target_fields = [
    # last_publication_date/index_date
    {'last_publication_date': r'"index_date":\W([\w+\W+]*?)\"'},
    # has_phone
    {'has_phone':r'"has_phone"\W+(\w+)'},
    # announce_id/list_id #both are 10 digit numbers
    {'annonce_id':r'"list_id"\W+(\d+)'},
    # type de bien
    {'type_de_bien':r'"Type de bien"\W+\w+\W+(\w+)'},
    # rooms
    {'rooms':r'"rooms"\W+\w+\W+(\d+)'},
    # area/surface
    {'area':r'"Surface"\W+\w+\W+([\d+\D+]*?)\"'},
    # ges
    {'GES':r'"GES"\W+\w+\W\:\"([\w+\W+]*?)\"'},
    # dpe/energy rate
    {'DPE':r'"energy_rate"\W+\w+\W\:\"([\w+\W+]*?)\"'},
    # furnished null
    {'Furnished':r'furnished'},
    # utilities #is null
    {'Utilities':r'utilities'},
    # details
    {'Details':r'(Honoraires|Référence)\W+\w+\W\:\"(\w+)\"'},
    # # "Sales_type/Category name"
    {'Sales_type': r'"category_name"\W+([\w+\W+]*?)\"'},
    # "Title/Subject",
    {'Subject':r'"subject"\:\"([\w+\W+]*?)\"'},
    # "Price /cost"
    {'Price':r'price\W+([\d+\D+]*?)\W'},
    # Currency
    {'Currency':r'Currency'},
    # Text/Body,W
    {'Body':r'body\W+([\w+\W+]*?)\"'},
    # City
    {'City': r'"city"\:\"([\w+\W]*?)"'},
    # postal_code
    {'Postal Code': r'"zipcode"\:"(\d+)"'},
    # latitude
    {'Lat': r'"lat"\:([\d+\.\d+]*)'},
    # longitude
    {'Lng':r'"lng"\:([\d+\.\d+]*)'},
    # department_name
    {'department name': r'"department_name"\:\"([\w+\W+]*?)\"'},
    # psuedo/name
    {'Psuedo': r'"name"\:\W([\w+\W+]*?)\"'},
    # photos
    {'Photos':r'"urls_large"\:\[([\W+\w+]*?)\]'},
    # department_id
    {'department_id': r'"department_id"\:\"(\d+)"'},
    # region name
    {'region_name':r'"region_name"\:\"([\w+\W+]*?)\"'},
    # advert_type/ad_type
    {'ad_type': r'"ad_type"\:\"([\w+]*?)\"'},
    # url
    {'url':r'"url"\:\"([\w+\W+]*?)"'},
    # first_publication_date
    {'first_publication_date':r'"first_publication_date"\:\W([\w+\W+]*?)\"'},
]


if __name__ == "__main__":
    # a list of user agents from which one will be randomly picked for every new request
    #Mozilla, Chrome, Opera Mini
    user_agents = [
         'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
         'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36',
         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.103'
          ]


    cookies = { }

    headers = { }

    page_count = 1 #used as counter and passed as url  page parameter
    csv_writer = Csvwriter('output.csv')

    #CURRENTY LOOKING FOR AN ALTERNATIVE TO THIS WHILE LOOP
    while page_count <= 4:
        print(f"FETCHING DATA FOR PAGE {page_count}....")
        # randomize user_agent per request
        user_agent = random.choice(user_agents)
        response = get_data(page_count,user_agent,headers,cookies)
        # gets x-path from request data
        data = get_x_path_data(response)
        # extracts fields from data in x_path and writes to csv file
        extract_and_save_annonce(data, page_count, target_fields,csv_writer)
        # increments counter so next request will go to next page until page 4
        print("page count: ", page_count, "\n")
        page_count += 1
        if page_count <= 4:
            interval = randint(5,15) #Randomize wait interval between requestss
            print(f"Resuming in {interval} seconds....")
            sleep(interval) 
        else:
            print("Exiting....")