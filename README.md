### Quick summary  ###

This is a Django powered web application for a hydroponics setup
run on a raspberry pi.

### Installation ###

NOTE: For [insert raspberry pi os here]

##### Clone and Setup Repository

```sh
# clone repo:
git clone https://github.com/psheppard16/hydroponics

# install pip requirements
cd hydroponics
pip install -r requirements.txt

# enter settings dir
cd hydro

# create settings_secret.py using template
cp settings_secret.py.template settings_secret.py

# Enter random characters for the 'SECRET_KEY' in `settings_secret.py`
SECRET_KEY='super random characters'

# return to repo root
cd ..

# collect static resources
gulp ("gulp watch" for continuous collection)
```

##### Database Configuration

For a local **SQLite** database add the following to `settings_secret.py`

```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

##### Database Setup

# Run migrations: 
python manage.py migrate

##### Run Test Server
`REMOTE_USER=admin python manage.py runserver`


### Documentation ###

Run `python manage.py open-docs` to open the documentation in your browser

##### Contributing

Documentation is written with [Sphinx](http://www.sphinx-doc.org/en/stable/). The .rst files are located in the `sphinx` folder.

Run `python manage.py build-docs` to build the documentation if you make changes.

### Testing ###

##### Run all tests:
```sh
driver=chrome REMOTE_USER=admin python manage.py --keepdb
```

##### Run specific test: 
```sh
driver=chrome REMOTE_USER=admin python manage.py --keepdb testing.test_changerequest.ChangeRequestTestCase.test_search
```