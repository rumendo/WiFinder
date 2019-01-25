import requests
import json
from bs4 import BeautifulSoup

cookie = {'key': '7fcb3ff5176fb532124b5ac3e4616a04'}

url = 'https://wpa-sec.stanev.org/?my_nets'

r = requests.get(url, cookies=cookie)

soup = BeautifulSoup(r.text, features="html.parser")

table = soup.find_all('table')

# table_head = [[cell.text for cell in row("th")]
#               for row in table]

table_data = [[cell.text for cell in row("td")]
              for row in table]

table_data = table_data[0]

data = [table_data[x:x+6] for x in range(0, len(table_data), 6)]

result = json.loads(json.dumps(data))

print(result[0][3])
