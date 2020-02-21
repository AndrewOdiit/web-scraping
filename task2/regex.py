import re


class RegexTester:
    def __init__(self):
        self.data = None
        with open('case.json', 'r', encoding='utf-8') as f:
            self.data = f.read()

    def match(self, regex: str):
        return re.findall(regex, self.data)


regexTester = RegexTester()
# Find the total number of private “Annonces” : “total_private”
print("Private Annonces: ", regexTester.match(
    r'\"total_private\"\:([0-9]+)'), "\n")
# link: https://regex101.com/r/fYFuCp/1

# Find the total number of pro “Annonces” : “total_pro”
print("total_pro's:", regexTester.match(r'\"total_pro\"\:(\d+)'), "\n")
# link: https://regex101.com/r/bCp8oB/1

# Find all the unique IDs of “Annonce” : “list_id”
print("list_ids: ", regexTester.match(r'\"list_id\"\:(\d+)'), "\n")
# link: https://regex101.com/r/ecLBZ9/1

# Find the prices : “price”
print("prices: ", regexTester.match(r'"price"\:\[\s+(\d+)\s+\]'), "\n")
# link: https://regex101.com/r/otuBdy/1

# Find the subject : “subject”
print("subjects: ", regexTester.match(r'\"subject\"\:([\W+\w+]*?)\,'), "\n")
# link: https://regex101.com/r/4MHaRb/1


# Find the number of rooms : “rooms”
print("rooms", regexTester.match(r'\"rooms\"\W+\w+\W+(\d+)'), "\n")
# link: https://regex101.com/r/WkCaEs/1

# Find lat
print("latitude", regexTester.match(r'\"lat\"\:(\d+\.\d+)'), "\n")
# link: https://regex101.com/r/Gjp59K/1


# Find lng
print("longitude", regexTester.match(r'\"lng\"\:(\d+\.\d+)'), "\n")
# link: https://regex101.com/r/YKeqhN/1
