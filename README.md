# Backend Major Project

## Introduction

This is our backend code for our major project.

## Setup

### Create a virtual environemnt

```bash
# For windows
python -m venv env

# For Linux
python3 -m venv env
```

### Install dependencies

To run this code you must be in the root folder of the project.

```bash
pip install -r requirements.txt
```

## Running the server

### Creating environment variables

Create a file named `.env` in the root folder of the project and copy the contents listed below

```
DOMAIN_URL=https://document-similarity-frontend.vercel.app/
DEBUG=True
ALLOWED_HOSTS=localhost
DJANGO_SECRET_KEY=django-insecure-y$1uddu@$n=v$qi1mszkk&5n9xygn%@_@+p^w#y7i05$w@d$$9
DB_NAME=kamao
DB_PASSWORD=Random4545
```

### Launching the server

First make sure you are inside the `backend` folder. Then run the following command

```bash
# For development
python manage.py runserver # Windows users
python3 manage.py runserver # Linux users

# For production
gunicorn backend.wsgi
```

> When using `gunicorn` the changes won't take effect with hot reload.
