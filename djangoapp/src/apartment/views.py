from django.shortcuts import render
from .models import apartment
from django.contrib import messages
from django.db import connection
from collections import namedtuple

# Create your views here.
def detail(request, ApartmentID):
    with connection.cursor() as c:
        c.execute("select * from apartment_apartment where ApartmentID = %s", [ApartmentID])
        result = namedtuplefetchall(c)
    return render(request, 'apartment/detail.html', {'info': result[0]})

# user collections.namedtuple() from the Python standard library
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]