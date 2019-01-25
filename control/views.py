from django.shortcuts import render
from django.http import HttpResponse
from control.scripts.hcx_control import hcx_start

def index(request):
    return render(request, 'control/home.html')


def start_hcx(request):
    hcx_start()

    return HttpResponse("""
    Maybe started.
    """)
