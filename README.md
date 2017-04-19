# Cumulus
Python-DJango cloud app

## Getting Started

To run the application you need a computer with any linux distribution.
You should have also installed python 2.7

### Requirements
```
Django==1.8.17
django-bootstrap3==6.2.2
```
### Installing
1. Download Cumulus
```
git clone https://github.com/sh4t4n/cumulus.git
```
2. Instaling requirements
```
cd cumulus
pip install -r requirements.txt
```
3. Create database and superuser
```
python manage.py migrate
python manage.py createsuperuser
```
4. Create home directory
```
mkdir path/to/directory
```
You must now specify a path in the settings.py file.
```
COMMANDER_ROOT_DIR = os.path.join(BASE_DIR, 'path/to/directory/')
```
### Running on development server
```
python manage.py runserver
```
Now you cane open "localhost:8000" 
