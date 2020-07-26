from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import UserRegisterForm
from collections import namedtuple


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

                INSERT INTO appUser_appuser (id, username, gender, bio, phone, num_of_post, user_id)
                VALUES ({1}, \"{2}\", \"{3}\", \"{4}\", \"{5}\", {6}, @cur_id);
             """.format(username, 0, username, gender, "", phone, 0))
            

            # display success msg
            messages.success(request, f'{username} - Your account has been created! You are now able to log in!')
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
            c1.execute("update appUser_appuser set bio = %s where username = %s", [savebio, currentuser])
            # value = namedtuplefetchall(c1)
        
    return render(request, 'appUser/profile.html', {})



