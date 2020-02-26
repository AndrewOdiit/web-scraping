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
    session.headers.update({'User-Agent':user_agent})
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
    else:
        print("error occured: ", response.status_code)

    assert tree is not None
    return tree.xpath("//body/script[5]/text()")[0]


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


    cookies = {
        '_gcl_au': '1.1.1572045614.1581602136',
        'cikneeto_uuid': 'id:fa1d0547-1bc4-4b71-8f3f-66daa7802b71',
        'xtvrn': '$562498$',
        'xtan562498': '-undefined',
        'xtant562498': '1',
        'ry_ry-l3b0nco_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwiZXhwIjoxNjEzMTM4MTQ1Mzc0LCJjcyI6bnVsbH0%3D',
        'saveOnboarding': '1',
        'cookieFrame': '2',
        'atidvisitor': '%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-562498-%22%2C%22an%22%3A%22NaN%22%2C%22ac%22%3A%220%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D',
        '_fbp': 'fb.1.1581918967107.705022993',
        '__gads': 'ID=4e95566f9daf183a:T=1581918989:S=ALNI_MaJRroLal4D6jRlXiTV-hZ62ptmVg',
        'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D48b945ef-5eb1-448f-bb7d-cfb45504236c-tuct4baa1ce',
        'abtest_user': '1',
        'nextSF': '1',
        'didomi_token': 'eyJ1c2VyX2lkIjoiMTcwM2VkNTYtOTBkZi02ZWQ5LWE5ODgtNWFmNWExY2IxYmM1IiwiY3JlYXRlZCI6IjIwMjAtMDItMTNUMTM6NTU6MzguNDU3WiIsInVwZGF0ZWQiOiIyMDIwLTAyLTI1VDA4OjU5OjUxLjg4MFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYW1hem9uIl0sImRpc2FibGVkIjpbXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llcyIsImFkdmVydGlzaW5nX3BlcnNvbmFsaXphdGlvbiIsImFkX2RlbGl2ZXJ5IiwiY29udGVudF9wZXJzb25hbGl6YXRpb24iLCJhbmFseXRpY3MiXSwiZGlzYWJsZWQiOltdfX0=',
        'euconsent': 'BOutVWIOvUNROAHABBFRC--AAAAuhr_7__7-_9_-_f__9uj3Or_v_f__32ccL59v_h_7v-_7fi_20nV4u_1vft9yfk1-5ctDztp507iakivXmqdeb9v_nz3_5pxPr8k89r7337Ew_v8_v-b7BCON_IAAAA',
        'ABTasty': 'uid%3D20021711084238872%26fst%3D1581926922538%26pst%3D1582626890329%26cst%3D1582719291371%26ns%3D19%26pvt%3D59%26pvis%3D1%26th%3D',
        'datadome': 'zcxI-Mpn-f~cGEkHEXKOod-i3LdIqha6sxwB.ytNh18q.KfsGi.0qw4IcpTzMxWznEaGAA53eiVCSX~8Q0iRiA7S4uYXC~0inMLfti6cZ',
        'cto_bundle': 'yPSNWF9sJTJCMkFYTHp2NlJ2YVZHYW5KS0dwaVV3MXdWV3h6bjZYM3hEMWMwNWhJdE1JZkNPJTJGZDdDSUgxbE9BeGRGZnpEYXlOaTdSa2klMkJNaWh1aW0lMkJNT0VWek1xWDMweDVCd0ZwMVJubXNRQW04SGtXeDBkdzZpNnNrRjlXaGRrZTliMFp5enh6YWxyUERleFZCTSUyRnlja2RPOU53JTNEJTNE',
        'ry_ry-l3b0nco_so_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D',
        '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1582720215894%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ.._VCpjWRnSrYurwXLXxl8rg.sSvaRfmplyBGej7Z5E9BSxMkUdsTS-GYkjqt_wK2UT37kNes7rwszuMTwWM4jo1q-wJJGCmLajmB9CbZx8HXi13o-2ktlB0Zi33EB_33tTax8QWpsAG3GWJaBvWgfzkhfaIT5YN_igRwl9a-TyEcfbZK7uspv57-JwFLvDL83lzshLyfZgENkMwMvkBE9qDJQ4OpW0cDXhYztwsC27oS-Q.VxyO1Fz9HvYBDrYN_zrzsA%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
        'ABTastySession': 'sen%3D5__referrer%3D__landingPage%3Dhttps%3A//www.leboncoin.fr/recherche/%3Fcategory%3D9%26locations%3DCassis%5C_13260%26page%3D1',
        'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:27$_ss:1$_st:1582721658845$_pn:1%3Bexp-session$ses_id:1582719301547%3Bexp-session',
        'cikneeto': 'date:1582719859276',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,fr;q=0.7',
    }

    params = (
        ('category', '9'),
        ('locations', 'Cassis_13260'),
        ('page', '1'),
    )

    response = requests.get('https://www.leboncoin.fr/recherche/', headers=headers, params=params, cookies=cookies)

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260&page=1', headers=headers, cookies=cookies)


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