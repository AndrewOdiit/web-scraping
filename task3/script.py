import requests
import json
import csv
from lxml import html
import requests
import re
import ast
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
    'oas_ab': 'a',
    'uuid': '2b21ce71-851a-4346-9635-5a6b75685003',
    '_fbp': 'fb.1.1581918967107.705022993',
    '__gads': 'ID=4e95566f9daf183a:T=1581918989:S=ALNI_MaJRroLal4D6jRlXiTV-hZ62ptmVg',
    'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D48b945ef-5eb1-448f-bb7d-cfb45504236c-tuct4baa1ce',
    'datadome': 'FAFOGRfW2nvannQc3_6Y8sgEKNDsy9sCznd1zbiVBv~mPP2BFHgRMeR5sV.n7bgxojtbzg6n~DOfk5T3Kxd3M9Z8zB72MLHXdpKKCEoQEV',
    '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1581927698393%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..sqaEx2L5SV6DOJd43qR08w.NXKJMIyvoXUU9zTf9gK5QfaYzNWMfboDuURh2JK4JwU6B8l4gPczrW7P0O6EnazOwhFF9xGYWaaoU80dmi34SuP1XyryHfx5fWV2pw3-CYmTlwtqToZ-jgHutLfXKNZIpI_slgFiFPhCk9weyQAOpw_eBXbHZrBpAjzev8JNVISxAjB_NekoAZSinNxMI11WNZInLvwAGYH0Y0BvxGwJlQ.nmUXIVuSeunZ92xJbnWGlg%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
    'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:8$_ss:0$_st:1581928644437',
    'cikneeto': 'date:1581926844544',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
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
)
tree = None
response = requests.get('https://www.leboncoin.fr/recherche/',
                        headers=headers, params=params, cookies=cookies)
if response.status_code == 200:
    # write to file
    tree = html.fromstring(response.content)
# do xPATH to script window.__REDIAL_PROPS__
# convert content to json
#
else:
    print("error occured: ", response.status_code)
assert tree is not None
data = tree.xpath("//body/script[5]/text()")[0]
data = str(data)
with open('dirty.txt', 'w', encoding='utf-8') as f:
    f.write(data)
    f.close()
# print(data.index("pivot"))
# data = data.split("],")  # this is probably fine
# # slice everything from null to pivot
# try to clean dataset
# print(json.dumps(data))
#data = data[1140:]
# the only way to search a string is through regular expressions
# Might be time for some regular expressions!!!!!s
# this list contains data that is not present in the demo.lxls file
patterns = [
    r'"images"\:\W+([\w+\W+]*?)\}\,',
    r'"body"\:\W+([\w+\W+]*?)\",',
    r'"location"\:([\W+\w+]*?)\}',
    r'"owner"\:\W+([\w+\W+]*?)\},',
    r'"options"\:([\W+\w+]*?)\}\,'
]

# # the clean function removes all fields not included in the provided output.xlsx file
# # assuming they are not needed


def clean(patterns: list, data_list: str):  # works fine
    target_string = data_list
    for pattern in patterns:
        target_string = re.sub(pattern, '', target_string)
    assert target_string != data_list
    return target_string


data = clean(patterns, data)

with open('clean.txt', 'w', encoding='utf-8') as f:
    f.write(data)
    f.close()

# # find last occurence of has phone
# # returns a list of indices of all occurrences of has_phone
# data = data.strip()
# print("after strip")
# last = [s.start() for s in re.finditer("}", data)][-2]
# # print(data[last])
# data = data[:last + 1]

# with open('clean.txt', 'w', encoding='utf-8') as f:
#     f.write(data)

checklist = re.findall(
    r'{(\"list_id"\:([\W+\w+]*?)\"has_phone"\:\w+\})', data)

# checklist = [r.strip(" ") for r in checklist]

print(len(checklist))
print(checklist[0])
