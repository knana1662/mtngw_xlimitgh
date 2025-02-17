### FEATURES

1. Refund Page
2. Logs Page
3. Admin Dashboard
4. Deployment with either Docker / Python's builtin zipapp
5. Load Database / Recover data from backup db
6. Backup database on every transactions
7. 

### IN PROGRESS

1. Load and import db using backup db
2. Use tables as sections
3. Use primary keys as sections under table
4. Use fields as headers
5. Include delete table
6. 

### FINISHED

### CODE

### EXCEPTION HANDLING

### REQUIREMENTS

Django>=5.1.1

pandas==2.2.2

python-dotenv==1.0.1

requests==2.32.3

plotly==5.22.0

docker==7.1.0

channels==4.1.0

daphne==4.1.2

pymemcache==4.0.0

gunicorn[gthread]

supervisor >=4.2.5

channels_redis

routeros_api

### VIRTUAL MACHINE (PLATFORM SPECIFIC)

###### LINUX & WINDOWS (WSL)

Run the following linux commands:

1. python3 -m venv .venv
2. cd ./venv/Scripts/activate
3. install "requirements.txt" file after  the virtual environment(.venv) is activated with this command  - pip install -r requirements.txt
4. sudo apt-get update
5. sudo apt install nginx postgresql redis memcached
6. python3 manage.py makemigrations
7. python3 manage.py migrate
8. python3 manage.py createsuperuser

   1. Enter username
   2. Enter email address
   3. Enter password
   4. Re-enter password
9. Add the following to settings.py file if not already present:

   1. DEBUG  = True  # Set to True if in development or False if in production
   2. ALLOWED_HOSTS = ["localhost","127.0.0.1"] # Set to ["localhost","127.0.0.1"] if in development or ["ipaddress" , "domain"] if in production . **NB:** Replace the "ipaddress" with the ipaddress of the production server and the "domain" with the domain name assigned to the ipaddress
   3. channel_layer = get_channel_layer("mem").group_send # Set to get_channel_layer("mem").group_send if in development or get_channel_layer("redis").send if in  production
   4. test_bundle = "0.1_GHS__100MB" # Set to "0.1_GHS__100MB" if in development(for testing purpose only) or "" (empty string) for production only
   5. get_all_data_allocations
   6. EMAIL_SUBJECT_PREFIX = "DDS CHILLZONE " # subject name to be used for the sending of emails to users, managers and admins of the site
   7. DEFAULT_FROM_EMAIL = "xyx@gmail.com" # email address to be used for the sending of emails to users, managers and admins of the site
   8. EMAIL_HOST_USER = "xyz" # * username of the email address to be used for the sending of emails to users, managers and admins of the site
   9. SERVER_EMAIL = "xyx@gmail.com" # email address to be used for the sending of emails to users, managers and admins of the site

### SOFTWARE ARCHITECTURE

Process Manager - Supervisor

CI / CD - Buildbot

API - FastAPI

DEPLOYMENT  - Docker

Logging - Sentry

WebSockets - Django Channels and Redis

Web Server - Gunicorn (For Backend) , Daphne(For Websockets) , Uvicorn (For API) and Nginx (For Load Balancing)

Backend - Django

Database - SQLite

Frontend - Tailwindcss , CSS , HTML , JS

Caching - Pymemcached

### CHANGES

###### 26.11.2024 (UPCOMING)

1. Use bulk create
2. Custom signal for handling the following:
   1. Request Finished
   2. Post Save
   3. Post Delete

###### 28.11.2024 (UPCOMING)

1. Additional Features:

   1. Navigation Urls
   2. API
   3. Business Intelligence
      1. Add Charts

###### **19.12.2024 (DONE)**

1. Increased admin dashboard page loading time to (0.04s - 4 seconds) by caching the charts
