import psycopg2
from django.conf import settings
import os
import django
import os
import sys
import psycopg2
sys.path.append('E:\\.internprj\\prjapp\\hlteam\\prjapp\\')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prjapp.settings")

# Import Django and configure the settings
import django
django.setup()

# Rest of your code to connect to the database and import the CSV file
# ...
import csv
import os
from django.conf import settings
import psycopg2

# Establish database connection
conn = psycopg2.connect(
    database=settings.DATABASES['default']['NAME'],
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['PASSWORD'],
    host=settings.DATABASES['default']['HOST'],
    port=settings.DATABASES['default']['PORT'],
)

# Open the CSV file
csv_file = open(os.path.join(settings.BASE_DIR, 'Players.csv'))
csv_reader = csv.reader(csv_file, delimiter=',')

# Create a cursor and execute SQL queries
cursor = conn.cursor()
for row in csv_reader:
    cursor.execute("INSERT INTO authentication_players (player_name, age, position, card, goals, dribbling, scoop, tackling, hit, sweep, air_tapping, gk_save_count, gk_recovery_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)


# Commit changes and close connections
conn.commit()
cursor.close()
conn.close()
csv_file.close()