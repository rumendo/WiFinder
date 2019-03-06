import requests
import json
from bs4 import BeautifulSoup
import psycopg2
import datetime

conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
cookie = {'key': '7fcb3ff5176fb532124b5ac3e4616a04'}
url = 'https://wpa-sec.stanev.org/?my_nets'
r = requests.get(url, cookies=cookie)

soup = BeautifulSoup(r.text, features="html.parser")

table = soup.find_all('table')
table_data = [[cell.text for cell in row("td")]
              for row in table]

table_data = table_data[0]
data = [table_data[x:x+6] for x in range(0, len(table_data), 6)]
result = json.loads(json.dumps(data))

json_data = {}
networks = []

for network in result:
    networks.append(network)

json_data["networks"] = networks

for idx, network in enumerate(json_data["networks"]):
    json_data["networks"][idx] =\
        {"id": network[0], "bssid": network[0], "ssid": network[1],
         "encryption": network[2], "psk": network[3], "last_updated": network[5]}

try:
    cur = conn.cursor()
    for network in json_data["networks"]:
        try:
            cur.execute("""INSERT INTO access_points (bssid, ssid, encryption, psk, location, last_updated)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (network['bssid'], network['ssid'], network['encryption'],
                            network['psk'], "42.69751, 23.32415", datetime.datetime.now()))
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()

    cur.close()
except Exception as e:
    print('ERROR:', e)
