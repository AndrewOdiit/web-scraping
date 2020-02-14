# I created this class in order to validate the different
# x paths for each question of number one
from lxml import html
import requests


class XPathTester:
    def __init__(self, url):
        assert url != None
        self.web_data = requests.get(url)  # retrieves data from case.html
        # converts data to a traversable html document
        self.tree = html.fromstring(self.web_data.content)

    def path_data(self, element_name, path):
        # This method returns the data at the specified x-path
        print("\n")
        print(f"*****PATH DATA AT XPATH for {element_name}*****\n")
        return self.tree.xpath(path)


if __name__ == "__main__":
    xpt = XPathTester("http://127.0.0.1:5500/leboncoin/task1/case.html")
 # Find xpath for Title of Annonce
    print(xpt.path_data(
        "Title of Annonce",
        '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/p/span/text()'))

# Find x path for price of Annonce
    price_data = xpt.path_data(
        "Price of Annonce",
        "//div[@class='l17WS bgMain']/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/div/span/span/text()")
    price_data = [r.rstrip("\xa0â\x82¬")
                  for r in price_data]
    print(price_data, "\n")


# Find XPath for kind of annonce (“Pro”, bold)
    kind_data = xpt.path_data(
        "Kind ('Pro',Bold) of Annonce",
        '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p/span/text()'
    )

    kind_data = [r.strip("()")for r in [r.rstrip("\xa0â\x82¬")
                                        for r in kind_data]]

    print(kind_data, "\n")


# Find XPath for type of annonce (“Ventes Immobilières”)
    type_data = xpt.path_data(
        "Type of Annonce (“Ventes Immobilières”)",
        '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p[1]/text()')
    print(list(filter(lambda x: x != '', [
          r.rstrip() for r in type_data])), "\n")

 # Find XPAth for city and zip data
city_zip_data = xpt.path_data(
    "Zip and City data of Annonce",
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p[2]/text()'
)
cities_and_zip_code = [r.split(" ") for r in city_zip_data]

print(cities_and_zip_code)

# 1.g Find XPath for date
date_data = xpt.path_data(
    "Date of Annonce",
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li[9]/a/section/div[2]/p[3]/text()'
)
print(date_data, "\n")
