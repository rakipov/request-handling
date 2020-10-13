from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from .settings import BUS_STATION_CSV
from urllib.parse import urlencode


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):

    count_page = 10
    data_bus_station = []

    with open(BUS_STATION_CSV, 'r', encoding='cp1251') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            item = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            data_bus_station.append(item)

    current_page = int(request.GET.get('page', 1))
    paginator = Paginator(data_bus_station, count_page)
    current_page = paginator.get_page(current_page)
    data_current_page = current_page.object_list

    if current_page.has_next():
        params = {'page': str(current_page.next_page_number())}
        next_page_url = '?'.join((reverse('bus_stations'), urlencode(params)))
    else:
        next_page_url = None

    if current_page.has_previous():
        params = {'page': str(current_page.previous_page_number())}
        prev_page_url = '?'.join((reverse('bus_stations'), urlencode(params)))
    else:
        prev_page_url = None
    return render(request, 'index.html', context={
        'bus_stations': data_current_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,

    })

