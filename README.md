# Play Roulette

Backend APIs for the casino game Play Roulette built using Django/Python, Django Rest Framework and MySQL.

## Installation

- Create a virtual environment in Python
- Install pip requirements `pip install -r requirements.txt`
- Create MySQL Database named `playroulette` and change configuration in `playroulette/playroulette/settings.py` if required.
- Migrate DB using `python manage.py migrate`
- Create superuser for admin using `python manage.py createsuperuser`, admin site can be viewed at `http://localhost:8000/admin`
- **Please add a payment gateway on admin site before recharging or cashing out balance to or from accounts in the admin platform**
- Start server using `python manage.py runserver`


## API Documentation

Please find the entire documentation here: https://documenter.getpostman.com/view/1308201/UVC5FSyu