import requests

cookies = {
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
    'ry_ry-l3b0nco_so_realytics': 'eyJpZCI6InJ5X0E4Rjk1NTU1LTAzRjQtNDI5NC1BNzVCLTk5QkJCQkFDQTU1QyIsImNpZCI6bnVsbCwib3JpZ2luIjp0cnVlLCJyZWYiOm51bGwsImNvbnQiOm51bGwsIm5zIjpmYWxzZX0%3D',
    '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1581919342032%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..xbJPTAvCbxctS0Yn10Cz9A.Ira-ygrWznGHSF1b9-FeVBtuYp1SMpPT3vNE2zic2ggybeKqE92xUnarjWfYAzYXhFe6kfW1ygQNLBOjs3zervC-c86Kd82q3MTJ-tR7r-ZR2BDZUX76OlR7PCjFwu5zF3uZsKMV7iaY4uuNW_sdto3ocdB_fpTtwpOJCZeucJZkBuBJHzXZyMkU9p7q6EprTYOLlI0hqi0M_uW2Lukr8A.WdYdqAuGj0BuY2xCLKqHew%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
    '_fbp': 'fb.1.1581918967107.705022993',
    '__gads': 'ID=4e95566f9daf183a:T=1581918989:S=ALNI_MaJRroLal4D6jRlXiTV-hZ62ptmVg',
    'cikneeto': 'date:1581919492450',
    'datadome': 'K9AcE.ETb0bP21bqXB5gUykUk-rYDJmk80EqJ1TihLWJtCBH7VKq7FEOILpuf28fN_wlOHY~hM~7eg~ylvcHUTmIf.8_WQB-~K6xPAbRGt',
    'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:8$_ss:0$_st:1581921297469$_pn:5%3Bexp-session$ses_id:1581918429835%3Bexp-session',
}

headers = {
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://www.leboncoin.fr',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.leboncoin.fr/ventes_immobilieres/1751365000.htm/',
    'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,fr;q=0.7',
}

response = requests.get(
    'https://api.leboncoin.fr/api/same/v2/search/1751365000', headers=headers, cookies=cookies)
print(response.content)
