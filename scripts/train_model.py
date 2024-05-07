import sys
import os
import django
import pandas as pd
from django.apps import apps
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib  # Adjust import based on your joblib version
from sklearn.pipeline import Pipeline

sys.path.append('E:\\.internprj\\prjapp\\hlteam\\prjapp\\')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prjapp.settings")
django.setup()

def get_model(team_name):
    """ Retrieves model class based on team name. """
    return apps.get_model('authentication', team_name)

def prepare_data(model_class):
    """ Fetches and prepares data from the database for the given model class. """
    data = model_class.objects.all().values(
        'possession_percentage', 'circle_count', 'shots_count',
        'field_goal', 'penalty_goal', 'penalty_corners', 'penalty_strokes', 'result'
    )
    return pd.DataFrame(data).dropna()

import os

def train_and_save():
    """ Trains and saves a model for each team. """
    model_directory = 'models'  # Path where models will be saved
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)  # Create the directory if it doesn't exist

    teams = ['WhiteWarriorszData', 'BlueBlazerzData', 'GreenGriffinzData', 
             'RedRufiianzData', 'VioletWhalezData', 'YellowYakzData']
    
    for team in teams:
        model_class = get_model(team)
        df = prepare_data(model_class)
        y = df.pop('result')
        X = df

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pipeline.fit(X_train, y_train)
        model_path = os.path.join(model_directory, f'{team.lower()}_model.pkl')
        joblib.dump(pipeline, model_path)

if __name__ == "__main__":
    train_and_save()
