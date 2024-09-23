import sys
import os
import django
import pandas as pd
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append('E:\\.internprj\\prjapp\\hlteam\\prjapp\\')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prjapp.settings")
django.setup()

from django.apps import apps

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

def train_and_evaluate():
    """ Trains and saves a model for each team, and prints out performance metrics. """
    model_directory = 'models'
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    teams = ['WhiteWarriorszData', 'BlueBlazerzData', 'GreenGriffinzData', 
             'RedRufiianzData', 'VioletWhalezData', 'YellowYakzData']
    
    for team in teams:
        logging.info(f"Processing {team}")
        model_class = get_model(team)
        df = prepare_data(model_class)
        y = df.pop('result')
        X = df

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(random_state=42))
        ])

        param_grid = {
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [None, 10, 20, 30],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4]
        }

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(pipeline, param_grid, cv=cv, scoring='accuracy', verbose=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        grid_search.fit(X_train, y_train)

        best_pipeline = grid_search.best_estimator_
        y_pred = best_pipeline.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        logging.info(f"Model for {team} - Best Params: {grid_search.best_params_}")
        logging.info(f"Model for {team} - Accuracy: {accuracy}")
        logging.info(f"Classification Report for {team}:\n{report}")
        logging.info(f"Confusion Matrix for {team}:\n{conf_matrix}")

        # Save the best model
        model_path = os.path.join(model_directory, f'{team.lower()}_model.pkl')
        joblib.dump(best_pipeline, model_path)
        plot_roc_curve(best_pipeline, X_test, y_test)
        plt.title(f'ROC Curve for {team}')
        plt.show()

        # Feature Importance (for tree-based models)
        if hasattr(best_pipeline.named_steps['classifier'], 'feature_importances_'):
            feature_importances = best_pipeline.named_steps['classifier'].feature_importances_
            sns.barplot(x=feature_importances, y=X.columns)
            plt.title(f'Feature Importances for {team}')
            plt.show()        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    train_and_evaluate()
