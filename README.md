# Assist-Co Server

## Setup

1. Install pip [Python's package manager](https://pip.pypa.io/en/stable/) by
- Downloading the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) file
- Then execute the file `python get-pip.py`
2. Install [VirtualEnv](https://virtualenv.pypa.io/en/stable/) Python's isolated virtual environment tool `sudo pip install virtualenv` This prevents collisions with OS Python packages
3. Clone the repository `git clone https://github.com/Assist-co/server.git`
- Change directory to the project `cd server`
4. Create a Pyton virtual environment and start it
- Enter `virtualenv venv` 
- Enter `source venv/bin/activate` To deactivate just enter `deactivate`
5. Install project packages. Enter `pip install -r requirements.txt`
6. Run migrations `python manage.py migrate` 
7. Load initial data `python manage.py loaddata seed.json`
8. Start the server `python manage.py runserver`!

## Tools

Assist-Co Server is based on the [Django-Rest-Framework](http://www.django-rest-framework.org)
