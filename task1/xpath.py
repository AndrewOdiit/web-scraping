from lxml import html
import requests
# I created this class in order to validate the different
# x paths for each question of number one
# This script reads from case.html, however it can  also read from remote host as well
# if provided with request headers,cookies -- use method read_from_remote
# and it would produce the same results in both cases


def read_data_from_file():
    data = None
    with open('case.html', 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()
    assert data is not None
    return data


def read_from_remote():
    # This method can make a request to remote host 'https://www.leboncoin.fr/recherche/*
    # however inorder to test the method , you must provide cookies and headers
    cookies = None
    headers = None

    assert cookies is not None
    assert headers is not None

    params = (
        ('category', '9'),
        ('locations', 'Cassis_13260'),
    )
    response = requests.get('https://www.leboncoin.fr/recherche/',
                            headers=headers, params=params, cookies=cookies)

    return response.content


class XPathTester:
    def __init__(self, readable_data):
        self._data = readable_data
        assert self._data is not None
        self.tree = html.fromstring(self._data)

    def _path_data(self, element_name, x_path):
        # This method returns the data at the specified x-path
        print("\n")
        print(f"*****DATA AT XPATH for {element_name}*****\n")
        return self.tree.xpath(x_path)

    def get_annonce_title(self):
        element_name = "Title of Annonce"
        path = "//p[@class='_2tubl']//text()"
        return self._path_data(element_name, path)

    def get_annonce_price(self):
        element_name = "Price of Annonce"
        path = "//div[@class='_2OJ8g']//span//text()"
        price_data = self._path_data(element_name, path)
        price_data = [r.strip()for r in [r.strip("\xa0â\x82¬")
                                         for r in price_data]]
        return price_data

    def get_annonce_kind(self):
        element_name = "Kind of Annonce"
        path = "//p[@class='CZbT3']/span[1]/text()"
        kind_data = self._path_data(element_name, path)
        return [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                       for r in kind_data]]

    def get_annonce_type(self):
        element_name = "Type of Annonce (“Ventes Immobilières”)"
        path = "//p[@class='CZbT3']/text()"
        type_data = self._path_data(element_name, path)
        type_data = [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                            for r in type_data]]
        return list(filter(lambda x: x != '', [
            r.rstrip() for r in type_data]))

    def get_annonce_city(self):
        element_name = "City data of Annonce"
        path = "//p[@class='_2qeuk']//text()"
        city_data = self._path_data(element_name, path)
        return [i[0] for i in [str(i).split(" ") for i in city_data]]

    def get_annonce_zip_code(self):
        element_name = "zip code data of Annonce"
        path = "//p[@class='_2qeuk']//text()"
        zip_data = self._path_data(element_name, path)
        return [i[1] for i in [str(i).split(" ") for i in zip_data]]

    def get_annonce_date(self):
        element_name = "Date of Annonce"
        path = "//p[@class='mAnae']/text()"
        return self._path_data(element_name, path)


if __name__ == "__main__":
    data = read_data_from_file()
    #data = read_from_remote()
    xpt = XPathTester(data)
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
