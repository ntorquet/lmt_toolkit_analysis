[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Made with Django](https://img.shields.io/badge/Made%20with-Django-blue)](https://www.djangoproject.com/)
[![Made with Django REST framework](https://img.shields.io/badge/Made%20with-Django%20REST%20framework-blue)](https://www.django-rest-framework.org/)
[![Made with Vuetify](https://img.shields.io/badge/Made%20with-Vuetify-1976D2)](https://vuetifyjs.com/)
[![Made with VueJS](https://img.shields.io/badge/Made%20with-VueJS-blue)](https://vuejs.org/)
[![Made with Nuxt](https://img.shields.io/badge/Made%20with-Nuxt-blue)](https://nuxt.com/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# lmt-toolkit

LMT-toolkit is an open source web application created to analyse Live Mouse Tracker (LMT) data easily and intuitively. LMT stores data in SQLite files that cannot be easily manipulated without some computer skills. 
LMT-toolkit makes it easy to compute and extract behavior profiles for each animal tested following a step-by-step process.

LMT-toolkit also provides a report of the reliability of your LMT experiments: you get information about the experimental environment (if you use temperature/humidity/sound/light sensor), and about the acquisition quality. 

Find more information about LMT on its [website](https://livemousetracker.org/) and [publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D).

LMT-toolkit uses analysis scripts that are constantly updated and improved.
We do our best to verify the accuracy of the results. It is your responsibility to check data accuracy.

## How to extract results

LMT-toolkit provides a step-by-step process:

### Select a SQLite file

First, select the LMT SQLite file you want to analyse:
![alt SQLite file selection](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_1_select_file.PNG?raw=true)

### Check the reliability

After the upload of the file, LMT-toolkit provides a report of the reliability of the experiment:

- information from temperature/humidity/sound/light sensor if you use it: this to check if the experimental environment was as expected during the experiment.
- comparison between number of frames recorded and expected: sometimes the computer lacks the resources needed for high-quality acquisition (when doing an update for example).
- percent of identification for each animal.
- percent of detection for each animal from RFID antennas.

As a whole, this information will tell you whether the experiment has been carried out under the expected experimental and material conditions.
![alt reliability](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_2_reliability.PNG?raw=true)

### Add animal information

You can add information about the animal (genotype, name, treatment, sex...). This information will be stored into the SQLite file and given in the result table.
![alt animal info](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_3_animal_info.PNG?raw=true)

### Rebuild the database

Before being extracted, behaviors must be fine-tuned. These rebuilt events are stored into the SQLite file.
![alt rebuild](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_4_rebuild.PNG?raw=true)

If the SQLite file is already rebuilt, you can skip this step.

### Configure the analysis

You can choose between two types of analysis: a global analysis (Simple preset) or a report of the activity per time bin (Activity preset).
![alt analysis config](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_5_analysis_config_v1-1-0.PNG?raw=true)

- If you choose the simple preset, by default the analysis will be done on the total duration of the experiment (see the [Behaviors extracted by LMT-toolkit table](#behaviors-extracted-by-lmt-toolkit) for more information). You can constrain the analysis by changing time limits. 
- If you choose the Activity preset, by default the time bin is set to 10 minutes. This analysis return the distance travelled in cm by each animal for each time bin over the entire duration of the experiment.

### Save the results

#### Simple preset

You can see the results divided in different tables, and download the whole in CSV format.
![alt simple prest](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_6_results.PNG?raw=true)

#### Activity preset

You can see the total distance travelled by each animal and a plot of the distance per time bin. You can download the data in CSV format.
![alt activity preset](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/screenshot_7_resultats_activitypertimebin.PNG?raw=true)

## Behaviors extracted by LMT-toolkit

| Name                       | Representation                                                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Total distance**         |                                                                                                                                                         | Total distance in meters travelled by the focus animal during all the experiment or between time limits.                                                                                                                                                                                                                                                                                   |
| **Single move**            | ![alt single move](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_moving.jpg?raw=true)               | The focal animal is moving (speed > 5 m/s) without being in contact with any other animal (total duration, number of events, mean duration of events).                                                                                                                                                                                                                                     |
| **Move in contact**        |                                                                                                                                                         | The focal animal is moving (speed > 5 m/s) while being in contact with another animal (total duration, number of events, mean duration of events).                                                                                                                                                                                                                                         |
| **Stop isolated**          |                                                                                                                                                         | The focal animal is resting (not moving) without being in contact with any other animal (total duration, number of events, mean duration of events).                                                                                                                                                                                                                                       |
| **Rear isolated**          | ![alt rearing](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_rearing.jpg?raw=true)                  | The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events). This event has to be validated!                                                                                                                               |
| **Rear in contact**        |                                                                                                                                                         | The focal animal is straightened on its hindlegs (either unsupported or against the wall). Rearing is considered when the body slope is higher than a threshold (total duration, number of events, mean duration of events). This event has to be validated!                                                                                                                               |
| **Contact**                | ![alt contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_cct.jpg?raw=true)                      | The focal animal is touching another individual (total duration, number of events, mean duration of events).                                                                                                                                                                                                                                                                               |
| **Group of 2**             |                                                                                                                                                         | The focal animal is touching one and only one other individual (total duration, number of events, mean duration of events). This event has to be validated!                                                                                                                                                                                                                                |
| **Group of 3**             |                                                                                                                                                         | The focal animal is touching two and only two other individuals (total duration, number of events, mean duration of events). This event has to be validated!                                                                                                                                                                                                                               |
| **Nose-nose**              | ![alt nose-nose](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_nose-nose.jpg?raw=true)              | The focal animal is sniffing the nose of another animal (i.e., the nose is at a whisker distance from the nose of the other animal) (total duration, number of events, mean duration of events).                                                                                                                                                                                           |
| **Nose-anogenital**        | ![alt nose-tail](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_nose-anogenital.jpg?raw=true)        | The focal animal is sniffing the ano-genital region of another animal (i.e., the nose is at a whisker distance from the tail basis of the other animal) (total duration, number of events, mean duration of events).                                                                                                                                                                       |
| **Side-side**              | ![alt side-side](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_side-side.jpg?raw=true)              | The flank of the focal animal is in contact with the flank of another animal; both animals head in the same direction (total duration, number of events, mean duration of events).                                                                                                                                                                                                         |
| **Side-side head-to-tail** | ![alt side-side opposite](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_side-side_opp.jpg?raw=true) | The flank of the focal animal is in contact with the flank of another animal; both animals head in opposite directions (total duration, number of events, mean duration of events).                                                                                                                                                                                                        |
| **Train 2**                | ![alt train2](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_train2.jpg?raw=true)                    | The focal animal is moving (speed > 5 m/s) while sniffing the ano-genital region of another animal also moving (total duration, number of events, mean duration of events).                                                                                                                                                                                                                |
| **Follow**                 |                                                                                                                                                         | The focal animal is walking in the path of another individual: the two animals are moving at a speed >5 cm/s, the angles between the two animals are less than 45° apart, and the mass centre of the follower (the focal animal) is within a follow zone of one mean body length of width and two mean body lengths of length (total duration, number of events, mean duration of events). |
| **Social approach**        | ![alt social approach](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_soc_app.jpg?raw=true)          | The focal animal gets closer to another one within a circular zone of 2 body lengths around the approached animal (total duration, number of events, mean duration of events).                                                                                                                                                                                                             |
| **Approach contact**       | ![alt approach contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_app_cct.jpg?raw=true)         | The focal animal gets closer to another one within a circular zone of two body lengths around the approached animal; the approach ends by a contact between the two animals (total duration, number of events, mean duration of events).                                                                                                                                                   |
| **Make group 3**           |                                                                                                                                                         | The focal animal is joining a group of two animals to form a group of three animals in contact (number of events). This event has to be validated!                                                                                                                                                                                                                                         |
| **Make group 4**           |                                                                                                                                                         | The focal animal is joining a group of three animals to form a group of four animals in contact (number of events). This event has to be validated!                                                                                                                                                                                                                                        |
| **Break contact**          | ![alt break contact](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/img_break_cct.jpg?raw=true)          | The focal animal is getting away (higher speed) from the animal it has been in contact with; the speed of the focal animal is higher than the speed of the other animal (number of events).                                                                                                                                                                                                |
| **Break group 3**          |                                                                                                                                                         | The focal animal is leaving a group of three animals to let a group of two animals in contact; the focal animal has the highest speed among the three animals in contact (number of events). This event has to be validated!                                                                                                                                                               |
| **Break group 4**          |                                                                                                                                                         | The focal animal is leaving a group of four animals, that remain as a group of three animals in contact; the focal animal has the highest speed among the four animals in contact (number of events). This event has to be validated!                                                                                                                                                      |

This table will be completed with each new behavior extraction possibility. This information is provided into LMT-toolkit (Documentation tab).

## Installation
[Installation via Docker](#docker-alternative-fullstack-installation)

LMT-toolkit needs Python 3.13.

LMT-toolkit works thanks to 3 different servers:

- a Django server with a REST API (Python)
- a Nuxt server for the frontend (the interface) (JavaScript - Vue)
- a Celery server to manage asynchronous tasks between the frontend and the Django server (Python)

![alt LMT-toolkit schema](https://github.com/ntorquet/lmt_toolkit_analysis/blob/main/lmt_toolkit_api/media/uploaded/img/lmt-toolkit_schema.png?raw=true)

It is recommended to create a [python virtual environment](https://docs.python.org/3/library/venv.html) into the root folder of the application to 
install the python required packages.

```
pip install virtualenv 
py -m venv venv
```

Launch the virtual environment to install requirements:

```
venv\Scripts\activate
```

On Linux/macOS:

```bash 
source .venv/bin/activate
```



[To run the 3 servers, we need 3 command prompts.](#How-to-launch-the-application-on-a-Windows-computer)

### Install the backend (Django with REST API)

Install LMT-toolkit_api and its dependencies:

```
cd lmt_toolkit_api
pip install -e .
```

### Database migration

```
python manage.py makemigrations
python manage.py migrate
```

### Load data for documentation and versions

```
python manage.py loaddata fixtures/export_data_v1_2.json
```

### Install the frontend (client)

To run LMT-toolkit client locally, a working LMT-toolkit API is required and the following tools have to be installed:
- [npm](https://www.npmjs.com/) (or [yarn](https://yarnpkg.com/))
- [nodejs](https://nodejs.org/)

#### Nuxt minimal starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

#### Setup

Make sure to install dependencies in the nuxt-api folder:

```bash
cd pathToTheLMTtoolkitFolder\nuxt-api
# npm
npm install
# or yarn
yarn install
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
So the original database remains unchanged.

### Launch the application

You need 3 terminal windows with administrator rights. Each of these terminals must remain open for the application to work.

#### Django server:

In the 1st terminal, go to the right folder (adapt the path according to the location of the application folder on your computer):

```cd pathToTheLMTtoolkitFolder\lmt_toolkit_analysis```

Activate the python virtual environment:

```venv\Scripts\activate```

Go to the lmt_toolkit_analysis folder:

```cd lmt_toolkit_api```

Launch the Django server:

```python manage.py runserver```

If this works, the lines below should appear:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### Celery server

In the second terminal, go to the right folder (adapt the path according to the location of the application folder on your computer):

```cd pathToTheLMTtoolkitFolder\lmt_toolkit_analysis```

Activate the python virtual environment:

```venv\Scripts\activate```

Go to the lmt_toolkit_analysis folder:

```cd lmt_toolkit_api```

Launch the Celery server:

```celery -A lmt_toolkit_analysis worker -l info -P solo```

#### 

#### Nuxt Vue.js server

In the 3rd terminal, go to the right folder (adapt the path according to the location of the application folder on your computer):

```cd pathToTheLMTtoolkitFolder\nuxt-api```

Launch the server:

```npm run dev```

Use [http://localhost:3000/](http://localhost:3000/) in your internet browser to use LMT-toolkit.



## Docker alternative fullstack installation

To install and launch LMT-toolkit via Docker, you have to install the [Docker environment or the Docker Desktop application](https://www.docker.com/) first.
Docker Desktop has to be launched with administrator rights.

1. Clone the repository:
   
   ```bash
   git clone https://github.com/ntorquet/lmt_toolkit_analysis.git
   ```

2.  Navigate to the lmt_toolkit_analysis folder and run the following command to build the Docker image and start all required services:
   
   ```bash
    docker compose up --build
   ```
   
   Use [http://localhost:3000/](http://localhost:3000/) in your internet browser to use LMT-toolkit.

### Docker Stop and Clean Up

To stop the running containers:

```bash
docker compose down
```

To stop and remove all containers, networks, and volumes created by Docker Compose:

```bash
docker compose down -v
```

To remove all unused Docker images and free up space (optional):

```bash
docker image prune -a
```

**⚠️ Warning:** `docker image prune -a` will remove **all** images not currently used by any container. Use it only if you're sure you don't need them anymore.





### Licence

LMT-toolkit analysis is released under the GPL v3.0 licence. See the [LICENSE](LICENSE) file.

Copyright (C) 2022 CNRS - INSERM - UNISTRA - ICS - IGBMC

LMT-toolkit uses the LMT-analysis code provided on [GitHub](https://github.com/fdechaumont/lmt-analysis). This code is also under the GPL v3.0 licence.

### Features attributions:

Code for LMT analysis on [GitHub](https://github.com/fdechaumont/lmt-analysis)

Mice in the different behavioural events drawn by P. Dugast (from the [Live Mouse Tracker publication](https://www.nature.com/articles/s41551-019-0396-1.epdf?shared_access_token=8wpLBUUytAaGAtXL96vwIdRgN0jAjWel9jnR3ZoTv0MWp3GqbF86Gf14i30j-gtSG2ayVLmU-s57ZbhM2WJjw18inKlRYt31Cg_hLJbPCqlKdjWBImyT1OrH5tewfPqUthmWceoct6RVAL_Vt8H-Og%3D%3D), DOI: [10.1038/s41551-019-0396-1](https://doi.org/10.1038/s41551-019-0396-1))

Mouse favicon created by [Good Ware - Flaticon](https://www.flaticon.com/free-icons/mice)