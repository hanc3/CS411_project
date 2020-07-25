- To Test the version locally, you need to:
```bash
# pull all changes
git pull

# switch to branch bzn
git checkout bzn

# Enter Virtual Env, install dependencies
pip install django-crispy-forms
pip install django-add-default-value

# after entering virtual env
cd src
```
- Under directory `src/`, start mysql `mysql.server start` if you haven't.
- CREATE necessary DATABASE(gorentuiuc_djangoapp_mysql) if you don't have those.
- Migrate if needed.
- Run server: `python manage.py runserver`
- Navigate to 'Sign Up+' at the top.
- Sign Up as a user.
- Go to 127.0.0.1:8000/admin To check if the new user appeared in AppUser

