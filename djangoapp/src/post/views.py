from django.shortcuts import render
from django.http import HttpResponse
from .models import post
from django.db import connection
from collections import namedtuple
from django.utils import timezone
from django.contrib import messages

# Create your views here.
# list the posts
def index(request):
    with connection.cursor() as c:
        c.execute("select Post_id, Post_title from post_post order by Pub_date desc")
        result = namedtuplefetchall(c)
    return render(request, 'post/post.html', {'postlist': result})

# detail of the post
def detail(request, Post_id):
    with connection.cursor() as c:
        c.execute("select * from post_post where Post_id = %s",[Post_id])
        result = namedtuplefetchall(c)
    return render(request, 'post/detail.html', {'info': result[0]})

def Insertrecord(request):
    if request.method=='POST':
        if request.POST.get('Post_title') and request.POST.get('id_id') \
            and request.POST.get('Apartment') and request.POST.get('Move_in_date')\
            and request.POST.get('Move_out_date') and request.POST.get('Price')\
            and request.POST.get('Bedroom') and request.POST.get('Bathroom') and request.POST.get('Duration'):
            
            # store the values
            saverecord=post()
            saverecord.Post_title = request.POST.get('Post_title')
            saverecord.id_id = request.POST.get('id_id')
            saverecord.Apartment = request.POST.get('Apartment')
            saverecord.Pub_date = timezone.now()
            saverecord.Move_out_date = request.POST.get('Move_out_date')
            saverecord.Move_in_date = request.POST.get('Move_in_date')
            saverecord.Price = request.POST.get('Price')
            saverecord.Bedroom = request.POST.get('Bedroom')
            saverecord.Bathroom = request.POST.get('Bathroom')
            saverecord.Duration = request.POST.get('Duration')

            # if there is Description
            if request.POST.get('Description'):
                saverecord.Description = request.POST.get('Description')
                with connection.cursor() as c:
                    c.execute(" insert into post_post(Post_title, id_id, Apartment, Pub_date, Move_out_date, Move_in_date, Price, Bedroom, Bathroom, Description, Duration)\
                                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.Apartment, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Description, saverecord.Duration])
            
            # no Description
            else:
                with connection.cursor() as c:
                    c.execute(" insert into post_post(Post_title, id_id, Apartment, Pub_date, Move_out_date, Move_in_date, Price, Bedroom, Bathroom, Duration)\
                                value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.Apartment, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Duration])
            messages.success(request, 'Post successfully')
            return render(request, 'post/insertpost.html')
        else:
            return render(request, 'post/insertpost.html')
    else:
        return render(request, 'post/insertpost.html')

# user collections.namedtuple() from the Python standard library
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
