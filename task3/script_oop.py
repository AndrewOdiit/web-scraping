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
    'cto_bundle': '-kv_uF9sJTJCMkFYTHp2NlJ2YVZHYW5KS0dwaWJ4T2pueDZxVG03SFlvdUpIVXFhVTNWdGR6Z3hmSmlIMjBxNCUyQnpmSjYzTCUyQkR3MXdYVkhNWENBWk5RdGFuNkM3bkZMYldydlBkZ29VbzRUUUZ3WWQ5SzVOJTJGRE1CVndId0dSVlBwUEFmJTJGNVhyd2NXcGhFaVBHRkNsUmZFeHFuMTZnJTNEJTNE',
    'ABTasty': 'uid=20021711084238872&fst=1581926922538&pst=1582820792357&cst=1584193987305&ns=24&pvt=68&pvis=3&th=',
    'datadome': 'Ma4QB96cNMuxAUGxqWfKdGPoxuEgxBH4~Z2nu~HoO-S2hcyuSg.XZIFuUcCgbfE.6Y5MeA3NGJ9jj3LtZ3Oar5.UI5iCm5CfsOCWbGFgC0',
    'ry_ry-l3b0nco_so_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D',
    '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1584194903166%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..fBo4JEdZAjQmwYiPNkGnig.58MV1m9q0WAKLAG2pUwNMzYbSKR0C3qcjrJdynHmcM2O2J6JdV4P4xLmDwaUSKLfxRGYjxoRJpwsYtllGvb-RqSPQp7wgUfDKiD94XrWE51Tl_x4rcoUCRuhExmtJhMpqVJL8SB-iZmsKGrOhl5LHMybxqzwW_1A401XBwYVisj-sB9qi5bWPtiK6D7siDgnM152QixEKmoAxtYoWZlBsA.SDbSAoTUMAqBcjNxRU7mvg%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
    'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:32$_ss:1$_st:1584195807478$_pn:1%3Bexp-session$ses_id:1584193997839%3Bexp-session',
    'cikneeto': 'date:1584194007563',
    'ABTastySession': 'mrasn=&lp=https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260&sen=2',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,fr;q=0.7',
    }
    
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
    {'first_publication_date':r'"first_publication_date"\:\W([\w+\W+]*?)\"'},\

            ]

    
    if len(cookies) < 1 or len(headers) < 1:
        sys.exit("****HEADERS AND COOKIES ARE REQUIRED TO MAKE REQUEST****")
    domain_names = "https://www.leboncoin.fr"
    spider = Spider(cookies,headers,domain_names)
    #Get links for all pages to visit
    spider.run(target_fields, "/recherche/?category=9&locations=Cassis_13260")

           
            

        