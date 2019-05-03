from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import psycopg2
import os
import time
import json


def home(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()

    if request.GET.get('port', ''):
        if request.GET.get('status', '') == '1':
            cur.execute("UPDATE devices SET status=2 WHERE ssh_port=" +
                        request.GET.get('port', '') + ";")
            command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '')\
                      + """ -o "StrictHostKeyChecking no" "echo '2' > /home/rumen/WiFinder/rpi_setup/status" """

        if request.GET.get('status', '') == '2':
            cur.execute("UPDATE devices SET status=1 WHERE ssh_port=" +
                        request.GET.get('port', '') + ";")
            command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '')\
                      + """ -o "StrictHostKeyChecking no" "echo '1' > /home/rumen/WiFinder/rpi_setup/status" """

        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        conn.commit()

    if request.GET.get('reboot', ''):
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('reboot', '')\
                  + """ -o "StrictHostKeyChecking no" "reboot" """
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    cur.execute("""SELECT * FROM devices ORDER BY id;""")
    result = cur.fetchall()
    json_data = {}
    devices = []

    for device in result:
        devices.append(device)

    json_data["devices"] = devices

    for idx, network in enumerate(json_data["devices"]):
        json_data["devices"][idx] = \
            {"id": network[0], "status": network[1],
             "mac_address": network[2], "ssh_port": network[3],
             "location": network[4], "last_changed": network[5]}

    cur.close()
    conn.close()
    return render(request, 'control/home.html', json_data)


def data(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()
    if request.GET.get('delete', ''):
        cur.execute("DELETE FROM access_points WHERE id=" +
                    request.GET.get('delete', '') + ";")
        conn.commit()

    cur.execute("""SELECT * FROM access_points ORDER BY id desc;""")
    result = cur.fetchall()

    json_data = {}
    networks = []

    for network in result:
        networks.append(network)

    json_data["networks"] = networks

    for idx, network in enumerate(json_data["networks"]):
        json_data["networks"][idx] = \
            {"id": network[0], "bssid": network[1],
             "ssid": network[2], "encryption": network[3],
             "psk": network[4], "location": network[5], "last_updated": network[6]}

    cur.close()
    conn.close()
    return render(request, 'control/data.html', json_data)


def networks(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()

    if request.GET.get('port', ''):
        # cur.execute("UPDATE devices SET status=3 WHERE ssh_port=" + request.GET.get('port', '') + ";")
        #
        # command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '')\
        #           + """ -o "StrictHostKeyChecking no" "echo '3' > /home/rumen/WiFinder/rpi_setup/status" """
        # subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        # time.sleep(10)

        if os.path.exists("/home/controller/networks.txt"):
            os.remove("/home/controller/networks.txt")

        command = """scp -P """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no" root@127.0.0.1:/home/rumen/WiFinder/rpi_setup/networks /home/controller/WiFinder/networks.txt"""
        subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

        with open('/home/controller/WiFinder/networks.txt') as json_file:
            networks = json.load(json_file)

        networks["networks"].pop(0)
        print(networks['networks'])

        json_data = {"networks": []}

        i = 0
        for network in networks["networks"]:
            if "2D1A" in networks["networks"][i][17]:
                networks["networks"][i][17] = "...IEEE 802.11i/WPA2 Version 1"
            elif "32043048606C" in networks["networks"][i][17]:
                networks["networks"][i][17] = "...Open"
            i += 1

        i = 0
        for network in networks["networks"]:
            json_data["networks"].append(
                {"bssid": network[0].replace(' ', '')[-17:], "ssid": network[5].replace(' ', '')[7:-1],
                 "channel": "Ch: " + network[1].replace(' ', '')[8:], "encryption": network[17].replace(' ', '')[3:],
                 "location": network[5].replace(' ', '')[7:-1], "ssh_port": request.GET.get('port', '')})
            i += 1


    conn.commit()
    return render(request, 'control/networks.html', json_data)


def data_map(request):
    return render(request, 'control/map.html')


def get_map_data(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM access_points;""")
    result = cur.fetchall()

    json_data = {}
    networks = []

    for network in result:
        networks.append(network)

    json_data["networks"] = networks

    for idx, network in enumerate(json_data["networks"]):
        json_data["networks"][idx] = \
            {"id": network[0], "bssid": network[1],
             "ssid": network[2], "encryption": network[3],
             "psk": network[4], "location": network[5], "last_updated": network[6]}

    cur.close()
    conn.close()

    return JsonResponse(json_data)


def location(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()
    if request.GET.get('delete', '') and request.GET.get('location', ''):
        cur.execute("UPDATE devices SET location=" + request.GET.get('location', '') +
                    " WHERE mac_address=" + request.GET.get('mac', '') + ";")
        conn.commit()
    return 0


def deauth_network(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller'"
                            "host='localhost' password='root'")
    cur = conn.cursor()

    if request.GET.get('bssid', '') and request.GET.get('port', ''):
        print(request.GET.get('bssid', ''), request.GET.get('port', ''))
        deauth = "python3 /home/rumen/WiFinder/rpi_setup/deauth.py "\
                 + request.GET.get('bssid', '')\
                 + " " + request.GET.get('channel', '')[4:]

        command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '')\
                  + """ -o "StrictHostKeyChecking no" """ + "\"" + deauth + "\""
        print(command)
        subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        time.sleep(30)

    if request.GET.get('port', ''):
        cur.execute("UPDATE devices SET status=2 WHERE ssh_port="
                    + request.GET.get('port', '') + ";")
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '')\
                  + """ -o "StrictHostKeyChecking no" "echo '2' > /home/rumen/WiFinder/rpi_setup/status" """
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    return 0
