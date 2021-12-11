import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Championship, Driver


# Create your views here.
def get_drivers(request):
    return HttpResponse(
        json.dumps([driver.get_dict() for driver in Driver.objects.all()]),
        content_type="application/json",
    )


def get_driver(request, driver_id):
    driver = Driver.objects.get(pk=driver_id)
    return HttpResponse(json.dumps(driver.get_dict()), content_type="application/json")


def leaderboard_page(request):
    context = {"championships": Championship.objects.all()}
    return render(request, "leaderboard/leaderboard_page.html", context=context)
