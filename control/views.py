from django.shortcuts import render
import subprocess
import psycopg2
import os
import time
import json


def home(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()

    if request.GET.get('port', ''):
        if request.GET.get('status', '') == '1':
            cur.execute("UPDATE devices SET status=2 WHERE ssh_port=" + request.GET.get('port', '') + ";")
            command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no"
            "echo '2' > /home/rumen/WiFinder/rpi_setup/status" """

        if request.GET.get('status', '') == '2':
            cur.execute("UPDATE devices SET status=1 WHERE ssh_port=" + request.GET.get('port', '') + ";")
            command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no"
            "echo '1' > /home/rumen/WiFinder/rpi_setup/status" """

        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        conn.commit()

    if request.GET.get('reboot', ''):
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('reboot', '') + """ -o "StrictHostKeyChecking no" "reboot" """
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
            {"id": network[0], "status": network[1], "mac_address": network[2],
             "ssh_port": network[3], "location": network[4], "last_changed": network[5]}

    # print(json_data)

    cur.close()
    conn.close()

    return render(request, 'control/home.html', json_data)


def data(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    if request.GET.get('delete', ''):
        cur.execute("DELETE FROM access_points WHERE id=" + request.GET.get('delete', '') + ";")
        conn.commit()

    cur.execute("""SELECT * FROM access_points;""")
    result = cur.fetchall()

    json_data = {}
    networks = []

    for network in result:
        networks.append(network)

    json_data["networks"] = networks

    for idx, network in enumerate(json_data["networks"]):
        json_data["networks"][idx] = \
            {"id": network[0], "bssid": network[1], "ssid": network[2],
             "encryption": network[3], "psk": network[4], "location": network[5], "last_updated": network[6]}

    # print(json_data)

    cur.close()
    conn.close()

    return render(request, 'control/data.html', json_data)


def networks(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    if request.GET.get('port', ''):
        cur.execute("UPDATE devices SET status=3 WHERE ssh_port=" + request.GET.get('port', '') + ";")
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no"
                    "echo '3' > /home/rumen/WiFinder/rpi_setup/status" """
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        time.sleep(10)

        if os.path.exists("/home/controller/networks"):
            os.remove("/home/controller/networks")

        command = """scp -P """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no"
        root@127.0.0.1:/home/rumen/WiFinder/rpi_setup/networks /home/controller"""
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        with open("/home/controller/networks") as json_file:
            networks = json.load(json_file)

    conn.commit()

    return render(request, 'control/networks.html', networks)


def data_map(request):
    return render(request, 'control/map.html')


def location(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    if request.GET.get('delete', '') and request.GET.get('location', ''):
        cur.execute("UPDATE devices SET location=" + request.GET.get('location', '') +
                    " WHERE mac_address="+ request.GET.get('mac', '') + ";")
        conn.commit()

    return 0


def deauth_network(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    
    if request.GET.get('bssid', '') and request.GET.get('port', ''):
        deauth = "python3 /home/rpi_setup/deauth -b " + request.GET.get('bssid', '') + " -c " + request.GET.get('channel', '')
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no" """ + deauth
        subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        time.sleep(60)

    if request.GET.get('port', ''):
        cur.execute("UPDATE devices SET status=2 WHERE ssh_port=" + request.GET.get('port', '') + ";")
        command = """ssh root@127.0.0.1 -p """ + request.GET.get('port', '') + """ -o "StrictHostKeyChecking no"
                    "echo '2' > /home/rumen/WiFinder/rpi_setup/status" """
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    return 0
