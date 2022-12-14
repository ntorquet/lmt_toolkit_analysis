[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# lmt_toolkit_analysis
LMT-toolkit analysis is an open source web application created to check the reliability of Live Mouse Tracker (LMT) experiments and to analyse LMT data.

Find more information about LMT on its [website](https://livemousetracker.org/) and [publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D).

LMT-toolkit uses analysis scripts that are constantly updated and improved.
We do our best to verify the accuracy of the results. It is your responsibility to check data accuracy.

## Licence
LMT-toolkit analysis is released under the GPL v3.0 licence. See the [LICENSE](LICENSE) file.

Copyright (C) 2022 CNRS - INSERM - UNISTRA - ICS - IGBMC

LMT-toolkit uses the LMT-analysis code provided on [GitHub](https://github.com/fdechaumont/lmt-analysis). This code is also under the GPL v3.0 licence.

## Python Requirements (See [requirements.txt](requirements.txt))
- Django==4.0.2
- djangorestframework==3.13.1
- django-filter==21.1
- djoser==2.1.0
- django-cors-headers==3.11.0
- django-celery
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
- networkx==2.8.5

Install this list with the command:
```
pip install -r requirements.txt
```

## Django installation
Create the Django project
```
django-admin startproject lmt_toolkit_analysis
```




## Javascript Requirements and installations
- vue-cli
- axios
- bootstrap-vue-3@0.3.12
- bootstrap-icons-vue
- vue3-popper
- chart.js (for plots)
- vue-chartjs (for plots)
- vue-toaster (for toasts)
- stylus-loader (for toasts)
- npm install vue-json-csv
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
npm i bootstrap-vue-3@0.3.12
npm i bootstrap-icons-vue
npm i vue3-popper
npm install vue-chartjs chart.js
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


## How to launch the application on a Windows computer
### :warning: Warning
Make sure you have enough space on your computer!

The application downloads the file: it makes a copy of it.
It then works on this copy and when the process is finished the copy is deleted. During the analysis, the application needs to store this copy.
So the original database remains unchanged. The changes made to the downloaded database during the analysis are not saved.

### Launch the application
You need 3 terminal windows (type cmd in the windows search bar). Each of these terminals must remain open for the application to work.

#### Django server:
In the 1st terminal, go to the right folder (adapt the path according to the location of the application folder on your compute):

```cd C:\Users\admin\Documents\GitHub\lmt_toolkit_analysis```

Activate the python virtual environment:

```venv\Scripts\activate```

Go to the lmt_toolkit_analysis folder:

```cd lmt_toolkit_analysis```

Launch the Django server:

```python manage.py runserver```

If this works, the lines below should appear:
```
System check identified no issues (0 silenced).
August 24, 2022 - 10:14:31
Django version 4.0.2, using settings 'lmt_toolkit_analysis.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```


#### Celery server
In the second terminal, go to the right folder (adapt the path according to the location of the application folder on your compute):

```cd C:\Users\admin\Documents\GitHub\lmt_toolkit_analysis```

Activate the python virtual environment:

```venv\Scripts\activate```

Go to the lmt_toolkit_analysis folder:

```cd lmt_toolkit_analysis```

Launch the Celery server:

```celery -A lmt_toolkit_analysis worker -l info -P solo```

If this works, the lines below should appear:
```
[2022-08-26 13:28:05,354: WARNING/MainProcess] No hostname was supplied. Reverting to default 'localhost'
 
 -------------- celery@PP2-1063-B v5.2.7 (dawn-chorus)
--- ***** -----
-- ******* ---- Windows-10-10.0.19042-SP0 2022-08-26 13:28:05
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         lmttoolkitanalysis:0x12a2dzkjhf20
- ** ---------- .> transport:   amqp://guest:**@localhost:5672//
- ** ---------- .> results:
- *** --- * --- .> concurrency: 16 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . lmt_toolkit_analysis.celery.debug_task
  . lmttoolkitanalysis.tasks.getReliability

[2022-08-26 13:28:05,402: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2022-08-26 13:28:05,408: INFO/MainProcess] mingle: searching for neighbors
[2022-08-26 13:28:05,413: WARNING/MainProcess] No hostname was supplied. Reverting to default 'localhost'
[2022-08-26 13:28:06,444: INFO/MainProcess] mingle: all alone
[2022-08-26 13:28:06,458: WARNING/MainProcess] C:\Users\admin\Documents\GitHub\lmt_toolkit_analysis\venv\lib\site-packages\celery\fixups\django.py:203: UserWarning: Using settings.DEBUG leads to a memory
            leak, never use this setting in production environments!
  warnings.warn('''Using settings.DEBUG leads to a memory

[2022-08-26 13:28:06,458: INFO/MainProcess] celery@PP2-1063-B ready.
```

#### Vue.js serveur
In the 3rd terminal, go to the right folder (adapt the path according to the location of the application folder on your compute):
```cd C:\Users\admin\Documents\GitHub\lmt_toolkit_analysis\lmt_toolkit_analysis\frontend```

Launch the server:
```npm run serve```

If this works, the lines below should appear:
```
  App running at:
  - Local:   http://localhost:3000/
  - Network: http://192.168.54.8:3000/
```

Use one of these url in your internet browser to use LMT-toolkit.


## Features attributions:
Code for LMT analysis on [GitHub](https://github.com/fdechaumont/lmt-analysis)

Mice in the different behavioural events drawn by P. Dugast (from the [Live Mouse Tracker publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D), DOI: [10.1038/s41551-019-0396-1](https://doi.org/10.1038/s41551-019-0396-1))

Mouse favicon created by [Good Ware - Flaticon](https://www.flaticon.com/free-icons/mice)