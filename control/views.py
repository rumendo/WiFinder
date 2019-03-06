from django.shortcuts import render
import psycopg2


def home(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM devices;""")
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

    print(json_data)

    return render(request, 'control/home.html', json_data)


def data(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
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
            {"id": network[0], "bssid": network[1], "ssid": network[2],
             "encryption": network[3], "psk": network[4], "location": network[5], "last_updated": network[6]}

    print(json_data)

    return render(request, 'control/data.html', json_data)


def data_map(request):
    return render(request, 'control/map.html')


def networks(request):
    return render(request, 'control/networks.html')


def clients(request):
    return render(request, 'control/clients.html')
