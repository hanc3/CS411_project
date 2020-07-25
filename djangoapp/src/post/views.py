from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import post
from django.db import connection
from collections import namedtuple
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
# user collections.namedtuple() from the Python standard library
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# list the posts
def index(request):
    with connection.cursor() as c:
        c.execute("select Post_id, Post_title, Description from post_post order by Pub_date desc")
        result = namedtuplefetchall(c)
    return render(request, 'post/post.html', {'postlist': result})

# detail of the post
def detail(request, Post_id):
    with connection.cursor() as c:
        c.execute("select * from post_post where Post_id = %s",[Post_id])
        result = namedtuplefetchall(c)
    return render(request, 'post/detail.html', {'info': result[0]})

@login_required(login_url='../../appUser/login')
def Insertrecord(request):
    # return apartment list
    with connection.cursor() as c:
        c.execute("select Name, ApartmentID from apartment_apartment")
        result = namedtuplefetchall(c)
    
    # form
    if request.method=='POST':
        if request.POST.get('Post_title') and request.POST.get('Duration') \
            and request.POST.get('ApartmentID') and request.POST.get('Move_in_date')\
            and request.POST.get('Move_out_date') and request.POST.get('Price')\
            and request.POST.get('Bedroom') and request.POST.get('Bathroom'):
            
            # store the values
            saverecord=post()
            saverecord.Post_title = request.POST.get('Post_title')
            saverecord.ApartmentID_id = request.POST.get('ApartmentID')
            saverecord.Pub_date = timezone.now()
            saverecord.Move_out_date = request.POST.get('Move_out_date')
            saverecord.Move_in_date = request.POST.get('Move_in_date')
            saverecord.Price = request.POST.get('Price')
            saverecord.Bedroom = request.POST.get('Bedroom')
            saverecord.Bathroom = request.POST.get('Bathroom')
            saverecord.Duration = request.POST.get('Duration')

            # id is the primary key of appUser, but request.user.id gets the id of auth_user table
            with connection.cursor() as c1:
                c1.execute("select id from appUser_appUser where user_id = %s", [request.user.id])
                user = namedtuplefetchall(c1)
            saverecord.id_id = user[0].id
            
            # find apartment name in the apartment table
            with connection.cursor() as c1:
                c1.execute("select Name from apartment_apartment where ApartmentID = %s",[saverecord.ApartmentID_id])
                apartment = namedtuplefetchall(c1)
            saverecord.Apartment = apartment[0].Name

            with connection.cursor() as c1:
                c1.execute("select Post_title from post_post\
                            where Post_title = %s and\
                                  ApartmentID_id = %s and\
                                  Move_out_date = %s and\
                                  Move_in_date = %s and\
                                  Price = %s and\
                                  Bedroom = %s and\
                                  Bathroom = %s and\
                                  Duration = %s and\
                                  id_id = %s",[saverecord.Post_title, saverecord.ApartmentID_id, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Duration, saverecord.id_id])
                value = namedtuplefetchall(c1)

            # check if the post exist
            if not value:
                # if there is Description
                if request.POST.get('Description'):
                    saverecord.Description = request.POST.get('Description')
                    with connection.cursor() as c:
                        c.execute(" insert into post_post(Post_title, id_id, ApartmentID_id, Pub_date, Move_out_date, Move_in_date, Price, Bedroom, Bathroom, Description, Duration, Apartment)\
                                    value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.ApartmentID_id, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Description, saverecord.Duration, saverecord.Apartment])
                
                # no Description
                else:
                    with connection.cursor() as c:
                        c.execute(" insert into post_post(Post_title, id_id, ApartmentID_id, Pub_date, Move_out_date, Move_in_date, Price, Bedroom, Bathroom, Duration, Apartment)\
                                    value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.ApartmentID_id, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Duration, saverecord.Apartment])

                # update number of post of the user
                with connection.cursor() as c:
                    c.execute(" update appuser_appuser\
                                set num_of_post = num_of_post + 1\
                                where id = %s", [saverecord.id_id])
            return redirect('../')
        else:
            return render(request, 'post/insertpost.html', {'apartments': result})
    else:
        return render(request, 'post/insertpost.html', {'apartments': result})

def Search(request):
    query = []
    value = []
    if request.method=='POST':
        if request.POST.get('Pet_friendly'):
            query.append('a.Pet_friendly = %s ')
            value.append(1)
        if request.POST.get('Swimming_pool'):
            query.append('a.Swimming_pool = %s ')
            value.append(1)
        if request.POST.get('Printer'):
            query.append('a.Printer = %s ')
            value.append(1)
        if request.POST.get('Gym'):
            query.append('a.Gym = %s ')
            value.append(1)

        order = request.POST.get('order')

        input_query = 'select * from post_post p left join apartment_apartment a on p.ApartmentID_id = a.ApartmentID '
        for i in range(len(query)):
            if (i == 0):
                input_query += 'where '
            input_query += query[i]
            if (i != len(query) - 1):
                input_query += 'and '
        input_query = input_query + 'order by ' + order
        with connection.cursor() as c:
            c.execute(input_query, value)
            result = namedtuplefetchall(c)
        return render(request, 'post/search_result.html', {'postlist': result})

    else:
        return render(request, 'post/search.html') 