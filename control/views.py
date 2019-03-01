from django.shortcuts import render
from django.http import HttpResponse
from control.scripts.hcx_control import hcx_start
import psycopg2
import psycopg2


def home(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM devices""")
    devices = cur.fetchall()
    print(devices)
    return render(request, 'control/home_example.html')


def data(request):
    return render(request, 'control/data.html')


def map(request):
    return render(request, 'control/map.html')


def networks(request):
    return render(request, 'control/networks.html')


def clients(request):
    return render(request, 'control/clients.html')
