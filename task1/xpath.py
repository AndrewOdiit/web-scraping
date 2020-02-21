from lxml import html
import requests
# I created this class in order to validate the different
# x paths for each question of number one
# Task 1  XPATH
# This script can either read from case.html or remote host at 'https://www.leboncoin.fr/recherche/'
# and it would produce the same results


class XPathTester:
    def __init__(self, req_type):
        self.req_type = req_type
        assert self.req_type is not None

        # converts data to a traversable html document
        self.tree = html.fromstring(self.make_request())

    def make_request(self):
        assert self.req_type is not None
        if(self.req_type != 'localhost' and self.req_type != 'remotehost'):
            raise ValueError(
                "invalid req_type ,must be either localhost or remote host")
        if self.req_type == 'localhost':
            response = requests.get(
                "http://127.0.0.1:5500/leboncoin/task1/case.html")
        elif self.req_type == 'remotehost':
            response = self.get_remote()
        assert response is not None
        if response.status_code == 401:
            return "Request is forbidden"

        return response.content

    def path_data(self, element_name, path):
        # This method returns the data at the specified x-path
        print("\n")
        print(f"*****PATH DATA AT XPATH for {element_name}*****\n")
        return self.tree.xpath(path)

    def get_annonce_title(self):
        element_name = "Title of Annonce"
        path = "//p[@class='_2tubl']//text()"
        return self.path_data(element_name, path)

    def get_annonce_price(self):
        element_name = "Price of Annonce"
        path = "//div[@class='_2OJ8g']//span//text()"
        price_data = self.path_data(element_name, path)
        price_data = [r.strip()for r in [r.strip("\xa0â\x82¬")
                                         for r in price_data]]
        return price_data

    def get_annonce_kind(self):
        element_name = "Kind of Annonce"
        path = "//p[@class='CZbT3']/span[1]/text()"
        kind_data = self.path_data(element_name, path)
        return [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                       for r in kind_data]]

    def get_annonce_type(self):
        element_name = "Type of Annonce (“Ventes Immobilières”)"
        path = "//p[@class='CZbT3']/text()"
        type_data = self.path_data(element_name, path)
        type_data = [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                            for r in type_data]]
        return list(filter(lambda x: x != '', [
            r.rstrip() for r in type_data]))

    def get_annonce_city(self):
        element_name = "City data of Annonce"
        path = "//p[@class='_2qeuk']//text()"
        city_data = self.path_data(element_name, path)
        return [i[0] for i in [str(i).split(" ") for i in city_data]]

    def get_annonce_zip_code(self):
        element_name = "zip code data of Annonce"
        path = "//p[@class='_2qeuk']//text()"
        zip_data = self.path_data(element_name, path)
        return [i[1] for i in [str(i).split(" ") for i in zip_data]]

    def get_annonce_date(self):
        element_name = "Date of Annonce"
        path = "//p[@class='mAnae']/text()"
        return self.path_data(element_name, path)

    def get_remote(self):
       # makes remote call to leboncoin.fr/*
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
            'cto_bundle': 'G1W9JF9sJTJCMkFYTHp2NlJ2YVZHYW5KS0dwaVdFcmVRYiUyRnREeU93TFklMkJEd3FMN2ZkbiUyQjkwZzFwcmZmemVMdWYwZkhsU2tNdkl4bzNjUGxhQ0Vhd0hwQnVjJTJGU3FFOGZSdVklMkJPJTJGYTNrSHUwb3RoT2NtVkxndm9laHFWbmw4SDNDbSUyRkl4S2ElMkYlMkJnZTBUUnVSN0dKS3dIZm11MnQ4ZyUzRCUzRA',
            'ABTasty': 'uid%3D20021711084238872%26fst%3D1581926922538%26pst%3D1582223966804%26cst%3D1582264880113%26ns%3D9%26pvt%3D32%26pvis%3D1%26th%3D',
            'datadome': '5bpoClWIQsnn_r65Fs6ekb-C8S_FvVUWdXsDuGppOAAOMB7v2kw3mjalPmRRLh4WanSDr~s.wEfIRCTSxXVa4zHebA-~rQy6E3qvtm69jo',
            '_pulse2data': '92e83110-2d91-4bb8-8310-02572f95d277%2Cv%2C%2C1582265794366%2CeyJpc3N1ZWRBdCI6IjIwMjAtMDItMTNUMTM6NTU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..uUscDL2DvEvNKdczQVIERw.RtEd1UyS6Rd-1YdwOfKMAmbRs5mHq7c_6In33rIQKgfQUhknQKYj2EmCoDg70FcbStQsEiiKjOja4Udu4_MkfKPg7flJFXfsLrw4Er7ps0xaSkxaUWDVnsGptuEwhYCvpNyF9Rioida8KfN5x-2syC-5h4UD9laGgLG6EkgzvYZpZhnymB-Ze-7V3toHJaAwVV7TWqnY66i8Yyy9edsAxQ.jFRHMVRaqRagDEnc-jdgIQ%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..QskdBilJSmSTMFEWFLumK_NubzQtVCX0rjiNEwtL73k',
            'utag_main': 'v_id:01703ed577b70017f38b29907dac03069004506100868$_sn:16$_ss:1$_st:1582266831617$_pn:1%3Bexp-session$ses_id:1582264888203%3Bexp-session',
            'cikneeto': 'date:1582265032304',
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

        response = requests.get('https://www.leboncoin.fr/recherche/',
                                headers=headers, params=params, cookies=cookies)
        return response


if __name__ == "__main__":
    # the constructor can either take an argument for remotehost or localhost
    # if a string thats is neither is entered ,it raises a ValueError

    # xpt = XPathTester(
    #     "remotehost")
    xpt = XPathTester(
        "localhost"
    )
    # Find xpath for Title of Annonce
    print(xpt.get_annonce_title())
    # Find x path for price of Annonce
    print(xpt.get_annonce_price())

    # Find XPath for kind of annonce (“Pro”, bold)
    print(xpt.get_annonce_kind())

    # Find XPath for type of annonce (“Ventes Immobilières”)
    print(xpt.get_annonce_type())

    # Find XPAth for city and zip data
    print(xpt.get_annonce_city())

    print(xpt.get_annonce_zip_code())
    # 1.g Find XPath for date
    print(xpt.get_annonce_date())
