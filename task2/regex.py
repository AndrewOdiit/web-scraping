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
print(regexTester.match(r'\"total_private\"\:(\d+)'), "\n")

# Find the total number of pro “Annonces” : “total_pro”
print("total_pro", regexTester.match(r'\"total_pro\"\:(\d+)'), "\n")


# Find all the unique IDs of “Annonce” : “list_id”
print("list_id: ", regexTester.match(r'\"list_id\"\:(\d+)'), "\n")


# Find the prices : “price”
print("price: ", regexTester.match(r'"price"\:\[\s+(\d+)\s+\]'), "\n")

# Find the subject : “subject”
print("subject: ", regexTester.match(r'\"subject\"\:(.*)'), "\n")

# Find the number of rooms : “rooms”
print("rooms", regexTester.match(r'\"rooms\"\W+\w+\W+(\d+)'), "\n")


# Find lat
print("latitude", regexTester.match(r'\"lat\"\:(\d+\.\d+)'), "\n")

# Find lng
print("latitude", regexTester.match(r'\"lng\"\:(\d+\.\d+)'), "\n")
