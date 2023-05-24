[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# lmt_toolkit_analysis
LMT-toolkit analysis is an open source web application created to check the reliability of Live Mouse Tracker (LMT) experiments and to analyse LMT data.

Find more information about LMT on its [website](https://livemousetracker.org/) and [publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D).

LMT-toolkit uses analysis scripts that are constantly updated and improved.
We do our best to verify the accuracy of the results. It is your responsibility to check data accuracy.

## Behaviors extracted by LMT-toolkit
| Name                   | Representation                                                                                                                                               | Description                                                                                                                                                                                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Total distance**     |                                                                                                                                                              | Total distance in meter travelled by the focus animal during all the experiment.      |
| **Single move**           | ![alt single move](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_moving.jpg?raw=true)               | The focal animal is moving (speed > 5 m/s) without being in contact with any other animal (total duration, number of events, mean duration of events). |
| **Move in contact**        |                                                                                                                                                              | The focal animal is moving (speed > 5 m/s) while being in contact with another animal (total duration, number of events, mean duration of events).                                                                                                           |
| **Stop isolated**          |                                                                                                                                                              | The focal animal is resting (not moving) without being in contact with any other animal (total duration, number of events, mean duration of events).                                                                                                         |
| **Rear isolated**          | ![alt rearing](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_rearing.jpg?raw=true)                  | The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events). This event has to be validated! |
| **Rear in contact**        |                                                                                                                                                              | The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events). This event has to be validated! |
| **Contact**                | ![alt contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_cct.jpg?raw=true)                      |The focal animal is touching another individual (total duration, number of events, mean duration of events).|
| **Group of 2**             |                                                                                                                                                              |The focal animal is touching one and only one other individual (total duration, number of events, mean duration of events). This event has to be validated!|
| **Group of 3**             |                                                                                                                                                              |The focal animal is touching two and only two other individuals (total duration, number of events, mean duration of events). This event has to be validated!|
| **Nose-nose**              | ![alt nose-nose](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_nose-nose.jpg?raw=true)              |The focal animal is sniffing the nose of another animal (i.e., the nose is at a whisker distance from the nose of the other animal) (total duration, number of events, mean duration of events).|
| **Nose-anogenital**        | ![alt nose-tail](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_nose-anogenital.jpg?raw=true)        |The focal animal is sniffing the ano-genital region of another animal (i.e., the nose is at a whisker distance from the tail basis of the other animal) (total duration, number of events, mean duration of events).|
| **Side-side**              | ![alt side-side](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_side-side.jpg?raw=true)              | The flank of the focal animal is in contact with the flank of another animal; both animals head in the same direction (total duration, number of events, mean duration of events).|
| **Side-side head-to-tail** | ![alt side-side opposite](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_side-side_opp.jpg?raw=true) |The flank of the focal animal is in contact with the flank of another animal; both animals head in opposite directions (total duration, number of events, mean duration of events).|
| **Train 2**                | ![alt train2](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_train2.jpg?raw=true)                    | The focal animal is moving (speed > 5 m/s) while sniffing the ano-genital region of another animal also moving (total duration, number of events, mean duration of events).|
| **Follow**                 |                                                                                                                                                              | The focal animal is walking in the path of another individual: the two animals are moving at a speed >5 cm/s, the angles between the two animals are less than 45° apart, and the mass centre of the follower (the focal animal) is within a follow zone of one mean body length of width and two mean body lengths of length (total duration, number of events, mean duration of events).|
| **Social approach**        | ![alt social approach](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_soc_app.jpg?raw=true)          | The focal animal gets closer to another one within a circular zone of 2 body lengths around the approached animal (total duration, number of events, mean duration of events).|
| **Approach contact**       | ![alt approach contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_app_cct.jpg?raw=true)         | The focal animal gets closer to another one within a circular zone of two body lengths around the approached animal; the approach ends by a contact between the two animals (total duration, number of events, mean duration of events).|
| **Make group 3**           |                                                                                                                                                              | The focal animal is joining a group of two animals to form a group of three animals in contact (number of events). This event has to be validated!|
| **Make group 4**           |                                                                                                                                                              | The focal animal is joining a group of three animals to form a group of four animals in contact (number of events). This event has to be validated!|
| **Break contact**          | ![alt break contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/img_break_cct.jpg?raw=true)          | The focal animal is getting away (higher speed) from the animal it has been in contact with; the speed of the focal animal is higher than the speed of the other animal (number of events).|
| **Break group 3**	         |                                                                                                                                                              | The focal animal is leaving a group of three animals to leave a group of two animals in contact; the focal animal has the highest speed among the three animals in contact (number of events). This event has to be validated!|
| **Break group 4**	         |                                                                                                                                                              | The focal animal is leaving a group of four animals, that remain as a group of three animals in contact; the focal animal has the highest speed among the four animals in contact (number of events). This event has to be validated!|

This table will be completed with each new behavior extraction possibility. This information is provided into LMT-toolkit (Documentation tab).

## How to extract results
LMT-toolkit provides a step-by-step process:

### Select a SQLite file
![alt SQLite file selection](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_1_select_file.PNG?raw=true)

### Check the reliability
![alt reliability](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_2_reliability.PNG?raw=true)

### Add animal information
These information will be stored into the SQLite file.
![alt animal info](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_3_animal_info.PNG?raw=true)

### Rebuild the database
Before being extracted, behaviors must be rebuilt. These events are stored into the SQLite file.
![alt rebuild](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_4_rebuild.PNG?raw=true)

### Configure the analysis
By default, the analysis will be done on the total duration of the experiment. You can limit the analysis.
![alt analysis config](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_5_analysis_config.PNG?raw=true)

### Save the results
You can see the results divided in different tables, and download the whole in CSV file.
![alt single move](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/screenshot_6_results.PNG?raw=true)


## Installation
LMT-toolkit works thanks to 3 different servers:
- a Django server with a REST API (Python)
- a Nuxt server for the frontend (the interface) (JavaScript - Vue)
- a Celery server to manage asynchronous tasks between the frontend and the Django server (Python)

![alt LMT-toolkit schema](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_analysis/media/uploaded/img/lmt-toolkit_schema.png?raw=true)

It is recommended to create a [python virtual environment](https://docs.python.org/3/library/venv.html) into the root folder of the application to 
install the python required packages.
[To run the 3 servers, we need 3 command prompts.](##How-to-launch-the-application-on-a-Windows-computer)

### Python Requirements (See [requirements.txt](requirements.txt))
- Django>=4.0.2
- djangorestframework==3.14
- django-filter==21.1
- djoser==2.1.0
- django-cors-headers==3.11.0
- Celery
- django-celery
- django-celery-results
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

### Database migration
```
python manage.py makemigrations
python manage.py migrate
```

### Load data for documentation and versions
```
python manage.py loaddata fixtures/datatostart.json
```



### Javascript Requirements and installations
First, you need to install a JavaScript runtime environment like [Node.js](https://nodejs.org/en). 
Then you will have to install these packages using npm or yarn package managers:
- nuxt
- axios
- vuetify@3.1.14
- pinia@2.0.34
- vue-chartjs@5.2.0
- chart.js (for plots)
- vue-chartjs (for plots)
- vue-json-csv

It is recommended to first rename the nuxt-frontend folder to first create a new nuxt application and 
then copy / past files from the previous nuxt-frontend to the new one.

```
npx nuxi@latest init nuxt-frontend
```
The above command will create a new nuxt application in a new nuxt-frontend folder.
You can then copy / paste all the folders and files from the previous nuxt-folder, except the .nuxt 
and the node_modules folders.
```
cd nuxt-frontend
npm i
```
Nuxt is now installed.

Then install the packages (example with npm):
```
npm install pinia @pinia/nuxt
npm i vuetify sass
npm i @mdi/font
npm install axios
npm install vue-chartjs chart.js
npm install vue-json-csv
```


### Celery
Celery is used to make asynchronous tasks.
We need a broker to make a pip between Celery and Django. It is possible to use [RabbitMQ](https://www.rabbitmq.com/).
On windows, RabbitMQ needs erlang to work:

https://erlang.org/download/otp_versions_tree.html

Download the latest version of erlang and install it.

Download RabbitMq and install it:

https://rabbitmq.com/install-windows.html

Once RabbitMQ is installed, it runs by itself and it is possible to access its terminal via the start menu (RabbitMQ Command Prompt).

If needed (normally it is created by default), create a new RabbitMQ user from this Command Prompt:

```rabbitmqctl add_user guest```

The two guests (user and password) are the ones found in the settings.py file of the Django application (already added)

```broker_url = 'amqp://guest:guest@localhost:5672//'```


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

```cd pathToTheLMTtoolkitFolder\lmt_toolkit_analysis```

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

```cd pathToTheLMTtoolkitFolder\lmt_toolkit_analysis```

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

#### Nuxt Vue.js server
In the 3rd terminal, go to the right folder (adapt the path according to the location of the application folder on your compute):
```cd pathToTheLMTtoolkitFolder\nuxt-frontend```

Launch the server:
```npm run dev```

If this works, the lines below should appear:
```
Nuxi 3.4.1                                                                                                                                                                                                                    16:12:58
Nuxt 3.4.1 with Nitro 2.3.3                                                                                                                                                                                                   16:12:58
                                                                                                                                                                                                                              16:12:59
  > Local:    http://localhost:3000/                                                                                                                                                                                                  
  > Network:  http://172.31.48.1:3000/                                                                                                                                                                                                
  > Network:  http://192.168.53.55:3000/       
```

Use one of these url in your internet browser to use LMT-toolkit.


### Licence
LMT-toolkit analysis is released under the GPL v3.0 licence. See the [LICENSE](LICENSE) file.

Copyright (C) 2022 CNRS - INSERM - UNISTRA - ICS - IGBMC

LMT-toolkit uses the LMT-analysis code provided on [GitHub](https://github.com/fdechaumont/lmt-analysis). This code is also under the GPL v3.0 licence.


### Features attributions:
Code for LMT analysis on [GitHub](https://github.com/fdechaumont/lmt-analysis)

Mice in the different behavioural events drawn by P. Dugast (from the [Live Mouse Tracker publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D), DOI: [10.1038/s41551-019-0396-1](https://doi.org/10.1038/s41551-019-0396-1))

Mouse favicon created by [Good Ware - Flaticon](https://www.flaticon.com/free-icons/mice)