Locksmith server
================

Simple server offering locking over the network over json RPC

Requirements
------------

 * Django 1.7
 * django-json-rpc

Installation
------------

* Install requirements:

```sh
$ pip install -r requirements.txt
```

* Setup project

```sh
$ vim settings.py
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py createsuperuser

```
* Launch server:

```sh
$ python manage.py runserver
```
