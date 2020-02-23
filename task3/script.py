import requests
import csv
from lxml import html
import re
from datetime import datetime
from time import sleep
from random import randint
import random
import sys

def get_data(page,user_agent):  
    # makes requests for page data
    session = requests.Session()
    session.headers.update({'User-Agent':user_agent})
    try:
        assert page is not None
        response = session.get(
        f'https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260&page={page}')
        return response
    except requests.HTTPError as e:
        sys.exit(e)
    except requests.ConnectionError as e:
        sys.exit(e)
    


def get_x_path_data(response): 
    #extract's desired data from reponse data using x_path
    if response.status_code == 200:

        tree = html.fromstring(response.content)
    else:
        print("error occured: ", response.status_code)

    assert tree is not None
    return tree.xpath("//body/script[5]/text()")[0]


def extract_and_save_annonce(data:list, page:int, fields:list): 
    #This function extracts annonce fields using a regex list and calls write_to_csv

    # Get all string structures that satisfy regex {list_id......has_phone: boolean}
    annonces = re.findall(
        r'{(\"list_id"\:[\W+\w+]*?\"has_phone"\:\w+)}', data)


    row = []  # represents a single row in csv
    # for all string structures/annonces, extract required fields
    for annonce in annonces:
        # apply each field-regex to each annonce to find data
        for field in fields:
            print("Pattern:", field)
            # find all matches of field in a  single annonce and return data
            res = re.findall(field, annonce)
            print(res)
            if len(res) < 1: #if no field is found
                if field != "(Currency)": # if field is currency
                    res.append((field, "NULL"))# append NULL / field not available
                   
                else:
                     res.append((field, "EURO")) # append EURO for currency
                    
            row.extend(res)  # add data to annonce/row 
            print("\n")
        # assert that row is not empty
        assert len(row) > 0
        # writes annonce to csv as row after all annonce fields have been appended
        write_to_csv(row,page)


def write_to_csv(data: list, page: int): 
    # This function writes the data to a csv file
    date = datetime.today().strftime('%Y-%m-%d') #get current date
    date_scraped = ('date_scraped', date)
    page_scraped = ('page_scraped', page)
    data.append(date_scraped)  # adds date_scraped to annonce
    data.append(page_scraped)  # adds page_scraped to annonce

    with open('output.csv', 'a',encoding='utf-8') as csv_file:
        ads_csv = csv.writer(csv_file)
        ads_csv.writerow(data)
        csv_file.close()


# A list of regular expressions used to extract the target fields
target_fields = [
    # last_publication_date/index_date
    r'"(index_date)":\W([\w+\W+]*?)\"',
    # has_phone
    r'"(has_phone)"\W+(\w+)',
    # announce_id/list_id #both are 10 digit numbers
    r'"(list_id)"\W+(\d+)',
    # type de bien
    r'"(Type de bien)"\W+\w+\W+(\w+)',
    # rooms
    r'"(rooms)"\W+\w+\W+(\d+)',
    # area/surface
    r'"(Surface)"\W+\w+\W+([\d+\D+]*?)\"',
    # ges
    r'"(GES)"\W+\w+\W\:\"([\w+\W+]*?)\"',
    # dpe/energy rate
    r'"(energy_rate)"\W+\w+\W\:\"([\w+\W+]*?)\"',
    # furnished null
    r'furnished',
    # utilities #is null
    r'utilities',
    # details
    r'"(Honoraires|Référence)"\W+\w+\W\:\"(\w+)\"',
    # # "Sales_type/Category name"
    r'"(category_name)"\W+([\w+\W+]*?)\"',
    # "Title/Subject",
    r'"(subject)"\:\"([\w+\W+]*?)\"',
    # "Price /cost"
    r'(price)\W+([\d+\D+]*?)\W',
    # Currency
    r'Currency',
    # Text/Body,W
    r'(body)\W+([\w+\W+]*?)\"',
    # City
    r'"(city)"\W+([\w+\W+]*?)\"',
    # postal_code
    r'"(zipcode)"\:"(\d+)"',
    # latitude
    r'"(lat)"\:([\d+\.\d+]*)',
    # longitude
    r'"(lng)"\:([\d+\.\d+]*)',
    # department_name
    r'"(department_name)"\:\"([\w+\W+]*?)\"',
    # psuedo/name
    r'"(name)"\:\W([\w+\W+]*?)\"',
    # photos
    r'"(urls_large)"\:\[([\W+\w+]*?)\]',
    # department_id
    r'"(department_id)"\:\"(\d+)"',
    # region name
    r'"(region_name)"\:\"([\w+\W+]*?)\"',
    # advert_type/ad_type
    r'"(ad_type)"\:\"([\w+]*?)\"',
    # url
    r'"(url)"\:\"([\w+\W+]*?)"',
    # first_publication_date
    r'"(first_publication_date)"\:\W([\w+\W+]*?)\"',
]

if __name__ == "__main__":
    #using both Mozilla and firefox
    user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
         'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36'
          ]

    page_count = 1 #used as counter and passed as url  page parameter
    # LOOKING FOR AN ALTERNATIVE TO THIS WHILE LOOP
    while page_count <= 4:
        print(f"FETCHING DATA FOR PAGE {page_count}....")
        # randomize user_agent per request
        user_agent = random.choice(user_agents)
        response = get_data(page_count,user_agent)
        # gets x-path from request data
        data = get_x_path_data(response)
        # extracts fields from data in x_path and writes to csv file
        extract_and_save_annonce(data, page_count, target_fields)
        # increments counter so next request will go to next page until page 4
        print("page count: ", page_count, "\n")
        page_count += 1
        if page_count <= 4:
            interval = randint(10,30) #Randomize wait interval between requestss
            print(f"Resuming in {interval} seconds....")
            sleep(interval) 
        else:
            print("Exiting....")


    