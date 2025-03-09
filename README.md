# Marvel Rivals Data Tracker

<img src="images/marvel_rivals.png" alt="logo" width=600 height=100%/>

This is a Django web-based application built with Python 3.x that helps track and analyze gameplay data for [Marvel Rivals](http://www.marvelrivals.com). It leverages Django ORM, Django REST Framework, and a PostgreSQL database to provide an engaging and insightful user experience for competitive players.

![Release](https://img.shields.io/github/v/release/anthonybturner/RivalsWatch?color=brightgreen)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.x-green)


 [RivalsWatch](https://rivalswatch.onrender.com/)
## Key Features
- **Django ORM**: Efficient database management using Django's Object-Relational Mapping system.
- **Django REST Framework**: API-driven architecture for handling game data and interactions.
- **PostgreSQL**: Robust, scalable database system for storing player stats, match data, and hero profiles.
- **Player Performance Tracking**: Analyze player win/loss patterns, track queues for winners and losers.
- **Hero Stats & Profiles**: Detailed hero stats and profiles with search functionality.
- **Match Analysis**: In-depth match analysis via video replays accessible through unique game IDs.
- **Engagement-Based Matchmaking (EOMM)**: Insights into whether the game uses EOMM for matchmaking.
- **Upcoming Features & News**: Stay updated on upcoming game features and news related to Marvel Rivals.

## Technologies Used
- **Python 3.x**
- **Django** (Web framework)
- **Django REST Framework** (API framework)
- **PostgreSQL** (Database)
- **JavaScript/HTML/CSS** (Frontend)

## Installation

### 1.  Clone the repository:
```bash
git clone https://github.com/yourusername/marvel-rivals-data-tracker.git 
cd marvel-rivals-data-tracker 
```

### 2.  Create the virtual environment and activate it
```bash 
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements
```bash 
pip install -r requirements.txt 
```

### 4.  Set up PostgreSQL database (ensure PostgreSQL is installed and running):
    Create a database for the project.
    Update the database settings in settings.py to match your PostgreSQL configuration.
```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5.  Apply migrations:
```python 
python manage.py makemigrations
python manage.py migrate
```

## 6.  Start the development server:
```python
python manage.py runserver
```

## 7.  Visit localhost
 `http://127.0.0.1:portnumber` in your browser to access the application.
 where **port number** is the port where the application is running locally
 By default, Django runs on port 8000, but you can change it if needed.
 e.g. [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
 
 

##  Usage
- **Search and view hero profiles**: Gain insight into hero stats, abilities, and strategies.
- **Matchmaking Analysis**: Examine patterns in match outcomes, player win/loss streaks, and analyze whether engagement-based matchmaking (EOMM) is utilized.
- **Video Replays**: Watch match replays by using unique game IDs for in-depth analysis of gameplay strategies.
- **Track your progress**: Log your matches and performance to see how you improve over time.

## Contributing
- Fork the repository
- Create a new branch `(git checkout -b feature-name)`
- Make your changes
- Commit your changes `(git commit -am 'Add feature')`
- Push to the branch `(git push origin feature-name)`
- Create a new Pull Request

## License ![LICENSE](https://img.shields.io/badge/license-MIT-green.svg)
