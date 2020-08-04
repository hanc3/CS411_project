from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import post
from django.db import connection
from collections import namedtuple
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
import datetime
import math


# Create your views here.
# user collections.namedtuple() from the Python standard library
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# list the posts
def index(request):
    exclude_post = []
    if request.user.is_authenticated:
        with connection.cursor() as c:
            c.execute("select id from appUser_appuser where user_id = %s", [request.user.id])
            user = namedtuplefetchall(c)
        id_id = user[0].id
        recommendation_result = recommend(id_id, 20, 15, 5, 1, 3, 0.4)
        for item in recommendation_result:
            exclude_post.append(item.Post_id)
        number = 5 - len(recommendation_result)
        top_view_result = top_views(number, exclude_post)
        for item in top_view_result:
            exclude_post.append(item.Post_id)
    else:
        top_view_result = top_views(5, exclude_post)
        for item in top_view_result:
            exclude_post.append(item.Post_id)
    
    query = []
    input_query = " select Post_id, Post_title, Description, Price\
                    from post_post "
    if exclude_post:
        input_query += 'where '
    for i in range(len(exclude_post)):
        input_query += ' Post_id != %s '
        if i != len(exclude_post) - 1:
            input_query += ' and '
    input_query += 'order by Pub_date desc'

    # print(input_query)
    # print(exclude_post)

    with connection.cursor() as c:
        c.execute(input_query, exclude_post)
        post = namedtuplefetchall(c)

    result = recommendation_result + top_view_result + post

    if request.method=='POST':
        if request.POST.get('search'):
            title = '%' + str(request.POST.get('search')) + '%'
            with connection.cursor() as c1:
                c1.execute("select Post_id, Post_title, Description\
                            from post_post\
                            where Post_title like %s\
                            order by Pub_date desc", [title])
                search_result = namedtuplefetchall(c1)
            return render(request, 'post/post.html', {'postlist': search_result})
        else:
            return render(request, 'post/post.html', {'postlist': result})
    else:
        return render(request, 'post/post.html', {'postlist': result})

# detail of the post
def detail(request, Post_id):
    with connection.cursor() as c:
        c.execute("drop view if exists post_detail")
        c.execute("create view post_detail as select * from post_post where Post_id = %s", [Post_id])
        c.execute("select * from post_detail p join apartment_apartment a on p.ApartmentID_id = a.ApartmentID;\
                   update post_post set Views = Views + 1 where Post_id = %s",[Post_id])
        result = namedtuplefetchall(c)
    with connection.cursor() as c:
        c.execute("drop view if exists post_detail")
    if request.user.is_authenticated:
        with connection.cursor() as c:
            c.execute("select id from appUser_appuser where user_id = %s", [request.user.id])
            user = namedtuplefetchall(c)
        id_id = user[0].id
        view_time = timezone.now()
        with connection.cursor() as c1:
            c1.execute("insert into post_view_history(id_id, Post_id_id, View_time) \
                        values(%s, %s, %s)", [id_id, Post_id, view_time])
                
    # join user + post
    with connection.cursor() as c2:
        c2.execute(""" 
            SELECT Users.username, Users.phone, Users.email FROM\
            (SELECT appUser_appuser.username AS username, appUser_appuser.phone AS phone, auth_user.email AS email, appUser_appuser.id AS id FROM appUser_appuser JOIN auth_user ON appUser_appuser.user_id = auth_user.id) AS Users\
            WHERE Users.id = {}
        """.format(result[0].id_id))
        user_info_list = namedtuplefetchall(c2)
        if len(user_info_list) > 0:
            user_info = user_info_list[0]

    return render(request, 'post/detail.html', {'info': result[0], 'user_info':user_info})

@login_required(login_url='../../appUser/login')
def Insertrecord(request):
    # return apartment list
    with connection.cursor() as c:
        c.execute("select Name, ApartmentID from apartment_apartment")
        result = namedtuplefetchall(c)
    
    date = str(dt.date(dt.now()))

    # form
    if request.method=='POST':
        if request.POST.get('Post_title') \
            and request.POST.get('ApartmentID') and request.POST.get('Move_in_date')\
            and request.POST.get('Move_out_date') and request.POST.get('Price')\
            and request.POST.get('Bedroom') and request.POST.get('Bathroom')\
            and request.POST.get('Move_out_date') > request.POST.get('Move_in_date'):
            
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
            date1 = datetime.datetime.strptime(saverecord.Move_out_date, "%Y-%m-%d").date()
            date2 = datetime.datetime.strptime(saverecord.Move_in_date, "%Y-%m-%d").date()
            saverecord.Duration = int(round((date1 - date2).days / 30))

            # id is the primary key of appuser, but request.user.id gets the id of auth_user table
            with connection.cursor() as c1:
                c1.execute("select id from appUser_appuser where user_id = %s", [request.user.id])
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
                                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.ApartmentID_id, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Description, saverecord.Duration, saverecord.Apartment])
                
                # no Description
                else:
                    with connection.cursor() as c:
                        c.execute(" insert into post_post(Post_title, id_id, ApartmentID_id, Pub_date, Move_out_date, Move_in_date, Price, Bedroom, Bathroom, Duration, Apartment)\
                                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[saverecord.Post_title, saverecord.id_id, saverecord.ApartmentID_id, saverecord.Pub_date, saverecord.Move_out_date, saverecord.Move_in_date, saverecord.Price, saverecord.Bedroom, saverecord.Bathroom, saverecord.Duration, saverecord.Apartment])

                # update number of post of the user
                with connection.cursor() as c:
                    c.execute(" update appUser_appuser\
                                set num_of_post = num_of_post + 1\
                                where id = %s", [saverecord.id_id])
            return redirect('../')
        else:
            return render(request, 'post/insertpost.html', {'apartments': result, 'date' : date})
    else:
        return render(request, 'post/insertpost.html', {'apartments': result, 'date' : date})

def Filter(request):
    # return apartment list
    with connection.cursor() as c:
        c.execute("select Name, ApartmentID from apartment_apartment")
        apartment = namedtuplefetchall(c)
    
    with connection.cursor() as c:
        c.execute("select Post_id, Post_title, Description from post_post order by Pub_date desc")
        result = namedtuplefetchall(c)
    query = []
    value = []
    history_query = []
    search = False
    if request.method=='POST':
        if request.POST.get('Pet_friendly'):
            query.append('a.Pet_friendly = %s ')
            value.append(1)
            history_query.append('Pet_friendly')
            search = True

        if request.POST.get('Swimming_pool'):
            query.append('a.Swimming_pool = %s ')
            value.append(1)
            history_query.append('Swimming_pool')
            search = True

        if request.POST.get('Printer'):
            query.append('a.Printer = %s ')
            value.append(1)
            history_query.append('Printer')
            search = True

        if request.POST.get('Gym'):
            query.append('a.Gym = %s ')
            value.append(1)
            history_query.append('Gym')
            search = True

        if request.POST.get('Price') and request.POST.get('Price') != '0':
            query.append('p.Price <= %s ')
            value.append(request.POST.get('Price'))
            history_query.append('Price')
            search = True

        if request.POST.get('Move_in_date'):
            query.append('p.Move_in_date <= %s ')
            value.append(request.POST.get('Move_in_date'))
            history_query.append('Move_in_date')
            search = True
        
        if request.POST.get('Move_out_date'):
            query.append('p.Move_in_date >= %s ')
            value.append(request.POST.get('Move_out_date'))
            history_query.append('Move_out_date')
            search = True

        if request.POST.get('Duration'):
            query.append('p.Duration = %s ')
            value.append(request.POST.get('Duration'))
            history_query.append('Duration')
            search = True

        if request.POST.get('Bathroom'):
            query.append('p.Bathroom = %s ')
            value.append(request.POST.get('Bathroom'))
            history_query.append('Bathroom')
            search = True
        
        if request.POST.get('Bedroom'):
            query.append('p.Bedroom = %s ')
            value.append(request.POST.get('Bedroom'))
            history_query.append('Bedroom')
            search = True

        if search is False:
            return render(request, 'post/filter_result.html', {'postlist': result, 'apartments': apartment})

        order = request.POST.get('order')

        input_query = 'select * from post_post p left join apartment_apartment a on p.ApartmentID_id = a.ApartmentID '
        for i in range(len(query)):
            if i == 0:
                input_query += 'where '
            input_query += query[i]
            if i != len(query) - 1:
                input_query += 'and '
        input_query = input_query + 'order by ' + order
        with connection.cursor() as c:
            c.execute(input_query, value)
            result = namedtuplefetchall(c)
        
        if request.user.is_authenticated:
            input_history = 'insert into post_search_history(id_id,Search_time,'
            input_value = ' values(%s,%s,'
            for i in range(len(history_query)):
                input_history += history_query[i]
                input_value += '%s'
                if (i != len(history_query) - 1):
                    input_history += ','
                    input_value += ','
            
            input_history = input_history + ')' + input_value + ')'
            with connection.cursor() as c:
                c.execute("select id from appUser_appuser where user_id = %s", [request.user.id])
                user = namedtuplefetchall(c)
            id_id = user[0].id
            search_time = timezone.now()
            value.insert(0, search_time)
            value.insert(0, id_id)
            with connection.cursor() as c1:
                c1.execute(input_history, value)
        return render(request, 'post/filter_result.html', {'postlist': result, 'apartments': apartment})

    else:
        return render(request, 'post/filter.html', {'apartments': apartment})

def top_views(number, recommend_post):
    start_time = timezone.now() - datetime.timedelta(days=45)
    query = []
    input_query = " select Post_id, Post_title, Description, Price\
                    from post_post\
                    where Pub_date > %s"
    for i in range(len(recommend_post)):
        input_query = input_query + ' and ' + ' Post_id != %s '
    input_query += 'order by Views desc limit %s'
    value = [start_time]
    value = value + recommend_post
    value.append(number)
    # print(input_query)
    # print(value)
    with connection.cursor() as c:
        c.execute(input_query, value)
        post = namedtuplefetchall(c)
    return post

def top_likes(number):
    start_time = timezone.now() - datetime.timedelta(days=45)
    with connection.cursor() as c:
        c.execute(" select Post_id, Post_title, Description, Price\
                    from post_post\
                    where Pub_date > %s\
                    order by Likes desc\
                    limit %s", [number, start_time])
        post = namedtuplefetchall(c)
    return post

def recommend(id_id, num_post, num_valid_post, num_search, num_valid_search, num_return_post, valid_percentage):
    valid_time = timezone.now() - datetime.timedelta(days=45)
    post_valid = False
    # validate post history
    with connection.cursor() as c:
        c.execute("drop view if exists history")
        c.execute(" create view history as\
                    select *\
                    from post_view_history\
                    where id_id = %s and View_time > %s\
                    order by View_time desc\
                    limit %s\
                    ",[id_id, valid_time, num_post])
        c.execute(" select count(View_time) as num\
                    from history")
        count = namedtuplefetchall(c)

    # post history is valid
    if count[0].num >= num_valid_post:
        with connection.cursor() as c:
            c.execute(" select sum(p.Price) as sum_price, sum(p.Bedroom) as sum_bedroom, sum(p.Bathroom) as sum_bathroom, count(h.View_time) as num\
                        from history h left outer join post_post p on h.Post_id_id = p.Post_id\
                        ")
            post_history = namedtuplefetchall(c)
        post_valid = True
    with connection.cursor() as c:
        c.execute("drop view if exists history")

    # validate search history
    with connection.cursor() as c:
        c.execute("drop view if exists history")
        c.execute(" create view history as\
                    select *\
                    from post_search_history\
                    where id_id = %s and Search_time > %s\
                    order by Search_time desc\
                    limit %s", [id_id, valid_time, num_search])
        c.execute(" select count(Search_time) as num\
                    from history")
        count = namedtuplefetchall(c)
    
    # recommend only base on post
    if count[0].num < num_valid_search:
        if post_valid is False:
            print("false")
            with connection.cursor() as c:
                c.execute("drop view if exists history")
            return []
        else:
            return_list = []
            price = math.floor(post_history[0].sum_price / post_history[0].num)
            bedroom = int(round(post_history[0].sum_bedroom / post_history[0].num))
            bathroom = int(round(post_history[0].sum_bathroom / post_history[0].num))
            print("price: " + str(price) + "; " + "bedroom: " + str(bedroom) + "; " + "bathroom: " + str(bathroom))
            with connection.cursor() as c:
                c.execute("drop view if exists history")
                c.execute(" select Post_id, Post_title, Description, Price \
                            from post_post\
                            where Price > %s and Price < %s and Bedroom = %s and Bathroom = %s\
                            order by Views desc\
                            limit %s", [price - 50, price + 50, bedroom, bathroom, num_return_post])
                posts = namedtuplefetchall(c)
            return posts
        
    with connection.cursor() as c:
        c.execute(" select min(Move_in_date) as move_in, max(Move_out_date) as move_out, sum(Duration) as sum_duration, count(Duration) as num_duration, sum(Price) as sum_price, count(Price) as num_price, sum(Bedroom) as sum_bedroom, count(Bedroom) as num_bedroom, sum(Bathroom) as sum_bathroom, count(Bathroom) as num_bathroom, count(Pet_friendly) as num_pet, count(Printer) as num_printer, count(Swimming_pool) as num_swimming, count(Gym) as num_gym, count(Search_time) as num\
                    from history")
        search_history = namedtuplefetchall(c)
    
    with connection.cursor() as c:
        c.execute("drop view history")
    
    query = []
    input_query = 'create view recommendation as select * from post_post where '
    value = []
    flag = False

    if search_history[0].move_in != None:
        query.append("Move_in_date > %s ")
        value.append(search_history[0].move_in - datetime.timedelta(days=5))
        flag = True
    
    if search_history[0].move_out != None:
        query.append("Move_out_date < %s ")
        value.append(search_history[0].move_out + datetime.timedelta(days=5))
        flag = True

    # eliminate post with duration, price, bedroom, bathroom
    if search_history[0].sum_duration != None:
        if search_history[0].num_duration / search_history[0].num > valid_percentage:
            duration = math.floor(search_history[0].num_duration / search_history[0].sum_duration)
            query.append("(Duration = %s or Duration = %s) ")
            value.append(duration)
            value.append(duration + 1)
            flag  = True

    if post_valid is False:
        if search_history[0].sum_price != None:
            if search_history[0].num_price / search_history[0].num > valid_percentage:
                price = math.floor(search_history[0].sum_price / search_history[0].num_price)
                query.append("price < %s ")
                value.append(price)
                flag = True
        
        if search_history[0].sum_bedroom != None:
            if search_history[0].num_bedroom / search_history[0].num > valid_percentage:
                bedroom = int(round(search_history[0].sum_bedroom / search_history[0].num_bedroom))
                query.append("Bedroom = %s ")
                value.append(bedroom)
                flag = True

        if search_history[0].sum_bathroom != None:
            if search_history[0].num_bathroom / search_history[0].num > valid_percentage:
                bathroom = int(round(search_history[0].sum_bathroom / search_history[0].num_bathroom))
                query.append("Bathroom = %s ")
                value.append(bathroom)
                flag = True
    else:
        flag = True
        if search_history[0].sum_price != None:
            if search_history[0].num_price / search_history[0].num > valid_percentage:
                price = math.floor((float(search_history[0].sum_price) / float(search_history[0].num_price)) * 0.7 +\
                        (float(post_history[0].sum_price) / float(post_history[0].num)) * 0.3)
            else:
                price = math.floor(float(post_history[0].sum_price) / float(post_history[0].num))
        else:
            price = math.floor(float(post_history[0].sum_price) / float(post_history[0].num))
        query.append("price < %s ")
        value.append(price)

        if search_history[0].sum_bedroom != None:
            if search_history[0].num_bedroom / search_history[0].num > valid_percentage:
                bedroom = int(round((float(search_history[0].sum_bedroom) / float(search_history[0].num_bedroom)) * 0.7 +\
                                     (float(post_history[0].sum_bedroom) / float(post_history[0].num)) * 0.3))
            else:
                bedroom = int(round(float(post_history[0].sum_bedroom) / float(post_history[0].num)))
        else:
            bedroom = int(round(float(post_history[0].sum_bedroom) / float(post_history[0].num)))
        query.append("Bedroom = %s ")
        value.append(bedroom)

        if search_history[0].sum_bathroom != None:
            if search_history[0].num_bathroom / search_history[0].num > valid_percentage:
                bathroom = int(round((float(search_history[0].sum_bathroom) / float(search_history[0].num_bathroom)) * 0.7 +\
                                     (float(post_history[0].sum_bathroom) / float(post_history[0].num)) * 0.3))
            else:
                bathroom = int(round(float(post_history[0].sum_bathroom) / float(post_history[0].num)))
        else:
            bathroom = int(round(float(post_history[0].sum_bathroom) / float(post_history[0].num)))
        query.append("Bathroom = %s ")
        value.append(bathroom)

    if flag is True:
        for i in range(len(query)):
            input_query += query[i]
            if i != len(query) - 1:
                input_query += 'and '
        with connection.cursor() as c:
            c.execute("drop view if exists recommendation")
            c.execute(input_query, value)
    else:
        with connection.cursor() as c:
            c.execute("drop view if exists recommendation")
            c.execute("create view recommendation as select * from post_post")
    # print(input_query)
    # print(value)
    with connection.cursor() as c:
        c.execute(" select Post_id, Post_title, Description, Price\
                    from (\
                        select r.Post_id, r.Post_title, r.Description, r.Price, (a.Pet_friendly * %s + a.Swimming_pool * %s + a.Printer * %s + a.Gym * %s) as score\
                        from recommendation r left outer join apartment_apartment a on r.ApartmentID_id = a.ApartmentID\
                    ) as sub\
                    order by score desc\
                    limit %s",\
                    [search_history[0].num_pet, search_history[0].num_swimming, search_history[0].num_printer, search_history[0].num_gym, num_return_post])
        posts = namedtuplefetchall(c)
        c.execute("drop view if exists recommendation")
    # print(posts)
    return posts
    