from django.shortcuts import render
from django.http import HttpResponse
from control.scripts.hcx_control import hcx_start
import psycopg2

hostname = 'localhost'
username = 'controller'
password = 'root'
database = 'wifinder'


def index(request):
    conn = psycopg2.connect("dbname='wifinder' user='controller' host='localhost' password='root'")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM devices""")
    devices = cur.fetchall()
    print(devices)

    return render(request, 'control/home.html')


def start_hcx(request):
    hcx_start()

    return HttpResponse("""
    Maybe started.
    """)
