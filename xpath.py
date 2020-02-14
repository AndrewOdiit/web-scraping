import codecs
from lxml import html
import requests

page = requests.get("http://127.0.0.1:5500/leboncoin/case.html")
assert page is not None
tree = html.fromstring(page.content)
assert tree is not None

# Find xpath for Title of Annonce
# returns a list of titles
print(tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/p/span/text()'
)[0])
# Find x path for price of Annonce
# returns an array of prices
print(tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[1]/div/span/span/text()'
)[0])
# Find XPath for kind of annonce (“Pro”, bold)
path = tree.xpath(
    '//div[@class="l17WS bgMain"]/div/div[6]/div/div/div/div[2]/ul/li/a/section/div[2]/p/span/text()'
)[0]
print(path)


# Find XPath for type of annonce (“Ventes Immobilières”)
