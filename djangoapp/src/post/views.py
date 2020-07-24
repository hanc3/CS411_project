from django.shortcuts import render
from django.http import HttpResponse
from .models import post
from django.db import connection
from collections import namedtuple

# Create your views here.
def index(request):
    with connection.cursor() as c:
        c.execute("select Post_id, Post_title from post_post order by Pub_date desc")
        result = namedtuplefetchall(c)
    return render(request, 'post.html', {'userlist': result})

def detail(request, Post_id):
    with connection.cursor() as c:
        c.execute("select * from post_post where Post_id = %s",[Post_id])
        result = namedtuplefetchall(c)
    return render(request, 'detail.html', {'info': result[0]})

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
