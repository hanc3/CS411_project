from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from .forms import UserRegisterForm, apartmentForm
from collections import namedtuple
from datetime import datetime


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

# Create your views here.
def register(request):
    # if it's a POST request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # save user(INTO auth-user NOT appUser)
            form.save()
        
            # get form info
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            gender = form.cleaned_data.get('gender')

            # Also write SQL Query to store it into appUser table
            cursor = connection.cursor()
            cursor.execute("""      
                SET @cur_id = -1;
                SELECT id INTO @cur_id FROM auth_user WHERE username = \'{0}\';

                INSERT INTO appuser_appuser (id, username, gender, bio, phone, num_of_post, user_id)
                VALUES ({1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", {6}, @cur_id);
             """.format(username, 0, username, gender, "", phone, 0))
            

            # display success msg
            messages.success(request, '{} - Your account has been created! You are now able to log in!'.format(username))
            return redirect('../login')
    else:
        # Empty Form
        form = UserRegisterForm()

    return render(request, 'appUser/register.html',{'form':form})


@login_required(login_url='../login')
def profile(request):
    savebio = ''
    currentuser = ''
    if request.method == 'POST':
        if request.POST.get('Bio'):
            savebio = request.POST.get('Bio')
            currentuser = request.user.username
        with connection.cursor() as c1:
            c1.execute("update appuser_appuser set bio = %s where username = %s", [savebio, currentuser])
            # value = namedtuplefetchall(c1)
        
    return render(request, 'appUser/profile.html', {})



def update(request):
    return render(request, 'appUser/update.html', {})

@login_required(login_url='../../appUser/login')
def post(request):
    with connection.cursor() as c1:
        c1.execute("select id from appuser_appUser where user_id = %s", [request.user.id])
        user = namedtuplefetchall(c1)
    id_id = user[0].id

    with connection.cursor() as c:
        c.execute("select Post_id, Post_title, Description from post_post where id_id = %s order by Pub_date desc", [id_id])
        result = namedtuplefetchall(c)

    if request.method=='POST':
        if request.POST.get('search'):
            title = '%' + str(request.POST.get('search')) + '%'
            with connection.cursor() as c1:
                c1.execute("select Post_id, Post_title, Description\
                            from post_post\
                            where Post_title like %s\
                                  and id_id = %s\
                            order by Pub_date desc", [title, id_id])
                search_result = namedtuplefetchall(c1)
            return render(request, 'appUser/post.html', {'postlist': search_result})
        else:
            return render(request, 'appUser/post.html', {'postlist': result})
    else:
        return render(request, 'appUser/post.html', {'postlist': result})

@login_required(login_url='../../appUser/login')
def editPost(request, Post_id):
    with connection.cursor() as c:
        c.execute("select Name, ApartmentID from apartment_apartment")
        apartment = namedtuplefetchall(c)
    with connection.cursor() as c:
        c.execute("select * from post_post where Post_id = %s",[Post_id])
        result = namedtuplefetchall(c)
    date = str(datetime.date(datetime.now()))
    move_in = str(result[0].Move_in_date)
    move_out = str(result[0].Move_out_date)
    query = []
    value = []
    if request.method=='POST':
        if request.POST.get('Post_title') and request.POST.get('Post_title') != result[0].Post_title:
            query.append('Post_title = %s ')
            value.append(request.POST.get('Post_title'))

        if request.POST.get('ApartmentID') and request.POST.get('ApartmentID') != result[0].ApartmentID_id:
            # find apartment name in the apartment table
            with connection.cursor() as c1:
                c1.execute("select Name from apartment_apartment where ApartmentID = %s",[request.POST.get('ApartmentID')])
                apartment = namedtuplefetchall(c1)
            query.append('ApartmentID_id = %s, Apartment = %s ')
            value.append(request.POST.get('ApartmentID'))
            value.append(apartment[0].Name)
        
        if request.POST.get('Description') and request.POST.get('Description') != result[0].Description:
            query.append('Description = %s ')
            value.append(request.POST.get('Description'))

        if request.POST.get('Move_in_date') and request.POST.get('Move_in_date') != result[0].Move_in_date:
            query.append('Move_in_date = %s ')
            value.append(request.POST.get('Move_in_date'))

        if request.POST.get('Move_out_date') and request.POST.get('Move_out_date') != result[0].Move_out_date:
            query.append('Move_out_date = %s ')
            value.append(request.POST.get('Move_out_date'))
        
        if request.POST.get('Price') and request.POST.get('Price') != result[0].Price:
            query.append('Price = %s ')
            value.append(request.POST.get('Price'))

        if request.POST.get('Bathroom') and request.POST.get('Bathroom') != result[0].Bathroom:
            query.append('Bathroom = %s ')
            value.append(request.POST.get('Bathroom'))
        
        if request.POST.get('Bedroom') and request.POST.get('Bedroom') != result[0].Bedroom:
            query.append('Bedroom = %s ')
            value.append(request.POST.get('Bedroom'))
        
        if len(query) != 0:
            input_query = "update post_post set "
            for i in range(len(query)):
                input_query += query[i]
                if (i != len(query) - 1):
                    input_query += ', '
            input_query += "where Post_id = %s"
            value.append(Post_id)
            print(input_query)
            with connection.cursor() as c:
                c.execute(input_query, value)
        
        return redirect('../../')

    return render(request, 'appUser/editPost.html', {'info': result[0], 'apartments':apartment, 'move_in': move_in, 'move_out': move_out, 'date': date})

@login_required(login_url='../../appUser/login')
def delete(request, Post_id):
    if request.method=='POST':
        with connection.cursor() as c:
            c.execute("delete from post_post where Post_id = %s", [Post_id])
        return redirect('../../')
    return render(request, 'appUser/deletePost.html')


# Only Super User can access
@user_passes_test(lambda u: u.is_superuser)
def editApartment(request):
    # if it's a POST request
    if request.method == 'POST':
        form = apartmentForm(request.POST)
        if form.is_valid():
            # get form info
            # String
            name = form.cleaned_data.get('apartment_name')
            desc = form.cleaned_data.get('description')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            addr = form.cleaned_data.get('address')
            # True/False (converted to 1/0)
            pet = int(form.cleaned_data.get('pet'))
            printer = int(form.cleaned_data.get('printer'))
            pool = int(form.cleaned_data.get('pool'))
            gym = int(form.cleaned_data.get('gym'))

            # Also write SQL Query to store it into apartment table
            cursor = connection.cursor()
            cursor.execute("""      
                INSERT INTO apartment_apartment (Name, Description, Location, Email, Phone, Pet_friendly, Printer, Swimming_pool, Gym)
                VALUES (\"{0}\", \"{1}\", \"{2}\", \"{3}\", \"{4}\", {5}, {6}, {7}, {8});
                """.format(name, desc, addr, email, phone, pet, printer, pool, gym))

    else:
        form = apartmentForm()
    return render(request, 'appUser/editApartment.html',{'form':form})