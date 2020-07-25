- To Test the version locally, you need to:
```bash
# pull all changes
git pull

# switch to branch bzn
git checkout xyt

# Enter Virtual Env, install dependencies
pip install django-crispy-forms
pip install django-add-default-value

# in djangoapp/settings.py INSTALLED_APPs add
'crispy_forms'

# after entering virtual env
cd src
```
- To add default value:
```bash
# https://pypi.org/project/django-add-default-value/
# Drop table need to add default value
python manage.py makemigrations

# in the 0001_initial.py
from django_add_default_value import AddDefaultValue

# inside operations add
AddDefaultValue(
  model_name='',
  name='',
  value='',
)

# migrate model
python manage.py migrate --fake model_name zero
python manage.py migrate model_name
```

- Under directory `src/`, start mysql `mysql.server start` if you haven't.
- CREATE necessary DATABASE(gorentuiuc_djangoapp_mysql) if you don't have those.
- Migrate if needed.
- Run server: `python manage.py runserver`
- Navigate to 'Sign Up+' at the top.
- Sign Up as a user.
- Go to 127.0.0.1:8000/admin To check if the new user appeared in AppUser
