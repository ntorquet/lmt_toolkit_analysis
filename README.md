# lmt_toolkit_analysis
A tool to check the reliability of Live Mouse Tracker (LMT) experiments and to analyse LMT data.

## Python Requirements (See [requirements.txt](requirements.txt))
- Django==4.0.2
- djangorestframework==3.13.1
- django-filter==21.1
- djoser==2.1.0
- django-cors-headers==3.11.0
- django-celery==3.3.1
- django-celery-results==2.3.0
- celery-progress==0.1.2
- psycopg2-binary
- affine==2.3.1
- numpy==1.23.1
- tabulate==0.8.10
- pandas==1.4.3
- matplotlib==3.5.2
- lxml==4.9.1
- psutil==5.9.1
- scipy==1.8.1
- seaborn==0.11.2
- statsmodels==0.13.2

Install this list with the command:
```
pip install -r requirements.txt
```

## Django installations
Create the Django project
```
django-admin startproject lmt_toolkit_analysis
```




## Javascript Requirements and installations
- vue-cli
- axios
- bootstrap-vue-3
- bootstrap-icons-vue
- vue3-popper
- chart.js (for plots)
- vue-toaster (for toasts)
- stylus-loader (for toasts)
```
npm install -g @vue/cli
vue create frontend
```
Select Manually select features.

Select (with the space bar) Babel, Router, Vuex et CSS Pre-processors. Unselect Linter / Formatter.

Vue version: select 3.x

 Use history mode for router? (Requires proper server setup for index fallback in production) (Y/n) -> Y

Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): (Use arrow keys) -> select Sass/SCSS (with dart-sass)

Where do you prefer placing config for Babel, ESLint, etc.? (Use arrow keys)   -> select In dedicated config files

Save this as a preset for future projects? (y/N) -> N


```
cd frontend
npm install axios
npm i bootstrap-vue-3
npm i bootstrap-icons-vue
npm i vue3-popper
npm install chart.js
npm install @meforma/vue-toaster
npm install stylus-loader@3 stylus
npm run serve
```

## Django configuration
### Django settings
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lmttoolkitreliability',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'django_celery_results',
    'celery_progress',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

At the end of the settings.py file, add:
```
broker_url = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = "Europe/Paris"
CELERY_IMPORTS = 'lmttoolkitanalysis.tasks'
CELERY_RESULT_BACKEND = 'django-db'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# To upload
MEDIA_URL = '/media/temp/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/temp/')
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, 'media/temp/')
```

### Database migration
```
python manage.py makemigrations
python manage.py migrate
```

### Start the server Django
```
python manage.py runserver
```

## Celery
Celery is used to make asynchronous tasks.

To start Celery, in the console, go to the application folder
```
cd lmt_toolkit_analysis
```
and then write this command:
```
celery -A lmt_toolkit_analysis worker -l info -P solo  
```



