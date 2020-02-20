import requests
import csv
from lxml import html
import requests
import re
import requests
from datetime import datetime


def get_data(page):
    assert page is not None
    cookies = {
        'crfgL0cSt0r': 'true',
        '_gcl_au': '1.1.1572045614.1581602136',
        'cikneeto_uuid': 'id:fa1d0547-1bc4-4b71-8f3f-66daa7802b71',
        'xtvrn': '$562498$',
        'xtan562498': '-undefined',
        'xtant562498': '1',
        'ry_ry-l3b0nco_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwiZXhwIjoxNjEzMTM4MTQ1Mzc0LCJjcyI6bnVsbH0%3D',
        'didomi_token': 'eyJ1c2VyX2lkIjoiMTcwM2VkNTYtOTBkZi02ZWQ5LWE5ODgtNWFmNWExY2IxYmM1IiwiY3JlYXRlZCI6IjIwMjAtMDItMTNUMTM6NTU6MzguNDU3WiIsInVwZGF0ZWQiOiIyMDIwLTAyLTEzVDE0OjIyOjAzLjY3M1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYW1hem9uIl0sImRpc2FibGVkIjpbXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llcyIsImFkdmVydGlzaW5nX3BlcnNvbmFsaXphdGlvbiIsImNvbnRlbnRfcGVyc29uYWxpemF0aW9uIiwiYWRfZGVsaXZlcnkiLCJhbmFseXRpY3MiXSwiZGlzYWJsZWQiOltdfX0=',
        'euconsent': 'BOutVWIOutZN0AHABBFRCv-AAAAstr_7__7-_9_-_f__9uj3Or_v_f__30ccL59v_B_zv-_7fi_20jV4u_1vft9yfk1-5ctDztp505iakivXmqdeb9v_nz3_5pxPr8k89r7337Ew_v8_v8b7BCIJ',
        'saveOnboarding': '1',
        'cookieFrame': '2',
        'atidvisitor': '%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-562498-%22%2C%22an%22%3A%22NaN%22%2C%22ac%22%3A%220%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D',
        '_fbp': 'fb.1.1581918967107.705022993',
        '__gads': 'ID=4e95566f9daf183a:T=1581918989:S=ALNI_MaJRroLal4D6jRlXiTV-hZ62ptmVg',
        'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D48b945ef-5eb1-448f-bb7d-cfb45504236c-tuct4baa1ce',
        'abtest_user': '1',
        'nextSF': '1',
        'ry_ry-l3b0nco_so_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D',
        '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1582181986928%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..ADQov7PhPZQGLRZpVEoT1w.JykEs2WDbIeOc6fCvu6P_126sZDBK3sDFwWugg8SBWNlS5gDn1hUWqZzMtirpRnyub69lkkkgDtc1rpkNlGXC6Pg96fukJ5HjoPVr4sCIyim0kvRSyWkhp-x7Sgqz3SOm7v6cvoJF1EBrsFrGRx4CqNre6P21vfU6_h8VHtw_nXWFb6xb8yLJhywK29pFVL10dfDUBWMjMeaZQKYv9jTGw.rC4x0WNRUP3rTvh-PRJ1Tw%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
        'ABTasty': 'uid%3D20021711084238872%26fst%3D1581926922538%26pst%3D1581936056856%26cst%3D1582181076199%26ns%3D3%26pvt%3D5%26pvis%3D2%26th%3D',
        'ABTastySession': 'sen%3D4__referrer%3D__landingPage%3Dhttps%3A//www.leboncoin.fr/',
        'datadome': 'b-.XJ9hUcXXPPpFv8RfxEpyGyzYKvUyiYwl_liG26~moN-aZufjQ0dN-tt2r.4F-TGw.78zxEYG_oZpacJMvrgt.alStZ3rteTl~HCzzw8',
        'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:11$_ss:0$_st:1582182904301$_pn:2%3Bexp-session$ses_id:1582181082892%3Bexp-session',
        'cikneeto': 'date:1582181104988',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,fr;q=0.7',
    }

    response = requests.get(
        f'https://www.leboncoin.fr/recherche/?category=9&locations=Cassis_13260&page={page}',
        headers=headers, cookies=cookies)
    return response


def get_x_path_data(response):
    if response.status_code == 200:

        tree = html.fromstring(response.content)
    else:
        print("error occured: ", response.status_code)

    assert tree is not None
    with open('dirty.txt', 'w', encoding='utf-8') as f:
        f.write(tree.xpath("//body/script[5]/text()")[0])
        f.close()
    return tree.xpath("//body/script[5]/text()")[0]

# Contains regular patterns that will be
# executed for each iteration of i inorder to
# extract the fields indicated in the sample extract,output.xlsx


def write_to_csv(data: list, date: datetime, page: int):
    # This function writes the data to a csv file
    date_scraped = ('date_scraped', date)
    page_scraped = ('page_scraped', page)
    data.append(date_scraped)
    data.append(page_scraped)
    with open('output.csv', 'a', newline='') as csv_file:
        ads_csv = csv.writer(csv_file)
        ads_csv.writerow(data)


def extract_and_save_data(data, page_scraped):
    # validates the structure of every string in the data list
    date = datetime.today().strftime('%Y-%m-%d')
    annonces = re.findall(
        r'{(\"list_id"\:[\W+\w+]*?\"has_phone"\:\w+)}', data)

    # O(N * 2) time complexity, will try to improve this
    row = []  # represents a single row in csv
    for i in annonces:
        print("***************")
        print("current i: ", annonces.index(i))
        for j in target_fields:
            print("Pattern:", j)
            res = re.findall(j, i)
            row.append(res)
            print(res)
            # right some custome code to flatten the output
            # migth use regex
            print("\n")
        assert len(row) > 0
        write_to_csv(row, date, page_scraped)


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
    r'"(furnished)"',
    # utilities #is null
    r'"(utilities)"',
    # details
    r'"(Honoraires|Référence)"\W+\w+\W\:\"(\w+)\"',
    # # "Sales_type/Category name"
    r'"(category_name)"\W+([\w+\W+]*?)\"',
    # "Title/Subject",
    r'"(subject)"\:\"([\w+\W+]*?)\"',
    # "Price /cost"
    r'(price)\W+([\d+\D+]*?)\W',
    # Text/Body,W
    r'(body)\W+([\w+\W+]*?)\"',
    # City
    r'"(city_label)"\W+([\w+\W+]*?)\"',
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
    # this needs to be done for all four pages
    page_count = 1
    while page_count <= 4:
        # gets data from site one page at a time
        response = get_data(page_count)
        # gets x-path from request data
        data = get_x_path_data(response)
        # extracts fields from data in x_path and writes to csv file
        extract_and_save_data(data, page_count)
        # increments counter so next request will go to next page until page 4
        print("page count: ", page_count)
        page_count += 1
