### Quick summary  ###

This is a Django powered web application for a hydroponics setup
run on a raspberry pi.

### Installation ###
NOTE: For Unix OS

##### Clone and Setup Repository
```sh
# clone repo:
`git clone https://github.com/psheppard16/hydroponics`

# install pip requirements
`cd hydroponics`
`pip install -r requirements.txt`

# install node requirements
`npm install`

# enter settings dir
`cd hydro`

# create settings_secret.py using template
`cp settings_secret.py.template settings_secret.py`

# Enter random characters for the 'SECRET_KEY' in `settings_secret.py`
SECRET_KEY='super random characters'

# return to repo root
`cd ..`

# collect static resources for main site
`gulp` (`gulp watch` for continuous collection)

# collect static resources for admin site
`python manage.py collectstatic`
```

##### Database Configuration
For a local **SQLite** database add the following to settings_secret.py

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
```sh
Make migrations: 
`python manage.py makemigrations`

Run migrations: 
`python manage.py migrate`
```

### Documentation

##### Contributing
```sh
Documentation is written with [Sphinx](http://www.sphinx-doc.org/en/stable/). 
The .rst files are located in the `sphinx` folder.

To open the documentation in your browser:
`python manage.py open-docs` 

To build the documentation after changes:
`python manage.py build-docs`
```

### Testing ###

##### Running tests locally
```sh
Run all tests:
`driver=chrome REMOTE_USER=admin python manage.py --keepdb`

Run specific tests: 
`driver=[driver] REMOTE_USER=admin python manage.py --keepdb testing.[test file].[test class].[test]`
```

### Production Server ###

#### Installation
```sh
Update apt-get:
`sudo apt-get update`

Install apache2, and wsgi:
`sudo apt-get install apache2 libapache2-mod-wsgi-py3`
```

#### Configutation
```sh
Enter settings dir:
`sudo nano /etc/apache2/sites-available/000-default.conf`

Add the following to the config file:

Alias /static [project path]/hydroponics/static
<Directory [project path]/hydroponics/static>
    Require all granted
</Directory>

<Directory [project path]/hydroponics/hydroponics>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>

WSGIDaemonProcess hydroponics python-path=[project path]/hydroponics python-home=[project path]/hydroponics/hydroponicsenv
WSGIProcessGroup hydroponics
WSGIScriptAlias / [project path]/hydroponics/hydroponics/wsgi.py
```

#### Permissions
```sh
Create group for apache, www-data, and all users
groupadd super_group
gpasswd -a apache super_group
gpasswd -a www-data super_group
gpasswd -a pi super_group   # if you have a user named pi
gpasswd -a foo super_group # if you have a user named foo
...

Give super_group permission to access the database:
`sudo chown super_group [project path]/hydroponics/db.sqlite3`
`sudo chown super_group [project path]/hydroponics`
`sudo chmod 664 [project path]/hydroponics/db.sqlite3`

Give super_group permission to access the logs:
`sudo chown super_group [project path]/hydroponics/logs/db_sql.log`
`sudo chown super_group [project path]/hydroponics/logs/status.log`
`sudo chown super_group [project path]/hydroponics/logs`
`sudo chmod 664 [project path]/hydroponics/logs/db_sql.log`
`sudo chmod 664 [project path]/hydroponics/logs/status.log`

Give super_group permission to access the GPIO pins:
`sudo chown www-data /dev/mem`
`sudo chmod g+rw /dev/mem`
```

#### Server Name
```sh
Add the name localhost to the new servername config file:
`echo "serverName localhost" | sudo tee /etc/apache2/conf-available/servername.conf

Enable the servername config file:
`sudo a2enconf servername

Reload apache:
`sudo service apache2 reload`

Reolad the apache daemon:
`systemctl daemon-reload`
```

#### Enabeling Changes
```sh
Restart apache to finalize configuration:
`sudo service apache2 restart`
```
    
#### Starting and Stopping the Server:
```sh
Start:
`sudo apachetcl start`

Stop:
`sudo apachetcl stop`

Restart:
`sudo apachetcl restart`
```