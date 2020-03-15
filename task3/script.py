from shadow_useragent import ShadowUserAgent
from time import sleep
from random import randint
import requests,sys
from lxml import html
import re,os,csv
from datetime import datetime
class Spider:
    def __init__(self,cookies, request_headers,domain_names):
        self.cookies = cookies
        self.request_headers = request_headers
        self.page_links = None
        self.visited = []
        self.domain_names = domain_names

    def _get_page_links(self,base_url:str):
        print("getting page links..")
        data = requests.get(domain_names + base_url,headers = headers,cookies=cookies)
        assert data is not None
        tree  = html.fromstring(data.content)
        pages = tree.xpath("//div//nav[@class ='nMaRG']//a//@href")
        #insert url for first page at front of url list
        pages.insert(0,base_url)
        print("pages: ",pages)
        assert pages is not None
        self.page_links = pages

    def run(self,target_fields,base_url):
        user_agent = ShadowUserAgent().chrome
        session = requests.Session() #may not need this
        session.headers.update({'user_agent':user_agent})# may not need this
        self._get_page_links(base_url)
        assert self.page_links is not None
        page = 1
        for link in self.page_links:
            if link not in self.visited:
                print(f"Fetching data for page {page}")
                data = self._crawl(link,session)
                print(f"Parsing data for page {page} ")
                parsed = self._parse_request_data(data)
                print(f"Processing parsed data for page {page} ")
                self._retrieve_and_save(parsed,target_fields,page)
                print(f"Page {page} data saved successfully... ")
                page += 1
                interval = randint(1,15)
                print(f"resuming in {interval} seconds... ")
                sleep(interval)
                self.visited.append(link)

        #sends request to specified url
        #this will loop over all urls and send requests to those
        #not in visited


    def _crawl(self,url,session):
        print(f"crawling...https://www.leboncoin.fr{url}")
        try:
            response = session.get(domain_names + url,
            headers=self.request_headers,cookies=self.cookies )
            assert response is not None
            assert response.status_code == 200
            print("response status:", response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            print("An error has occured: ", e)
            sys.exit(e)

    def _parse_request_data(self,data):
        #update pages list
        #extracts desired data from response
        tree = html.fromstring(data.content)
        assert tree is not None
        annonce_data =  tree.xpath("//body/script[5]/text()")[0]
        assert annonce_data is not None
        return annonce_data

    def _retrieve_and_save(self,data,target_fields:dict, page):
        #This function extracts annonce fields using a regex list and calls write_to_csv

        # Get all string structures that satisfy regex {list_id......has_phone: boolean}
        annonces = re.findall(
            r'{(\"list_id"\:[\W+\w+]*?\"has_phone"\:\w+)}', data)

        headers = [list(i.keys())[0] for i in target_fields] #get headers
        headers.extend(['date_scraped','page_scraped'])
        fields = [list(i.values())[0] for i in target_fields] #get fields
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
        self.save(rows,page,headers)

    def save(self, data: list, page: int, headers:list):
        file_exists = os.path.isfile('output.csv')
        with open('output.csv','a') as f:
            csv_writer = csv.DictWriter(f,fieldnames=headers)
            if not file_exists:
                csv_writer.writeheader()
            csv_writer.writerows(data)


if __name__ =="__main__":
    cookies = {}

    headers = {}
    
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

    
    if len(cookies) < 1 or len(headers) < 1:
        sys.exit("****HEADERS AND COOKIES ARE REQUIRED TO MAKE REQUEST****")
    domain_names = "https://www.leboncoin.fr"
    spider = Spider(cookies,headers,domain_names)
    #Get links for all pages to visit
    spider.run(target_fields, "/recherche/?category=9&locations=Cassis_13260")

           
            

        