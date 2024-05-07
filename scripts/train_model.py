import sys
import os
import django
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib  # Adjust import based on your joblib version
from django_pandas.io import read_frame
from sklearn.compose import ColumnTransformer

# Ensure that Django settings are configured properly for standalone scripts
sys.path.append('E:\\.internprj\\prjapp\\hlteam\\prjapp\\')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prjapp.settings")
django.setup()

from authentication.models import WhiteWarriorszData

def prepare_data():
    qs = WhiteWarriorszData.objects.all()
    df = pd.DataFrame.from_records(qs.values(
        'possession_percentage', 'circle_count', 'shots_count', 
        'field_goal', 'penalty_goal', 'penalty_corners', 'penalty_strokes', 'result'
    ))
    df.fillna(df.mean(), inplace=True)  # Handle missing values
    return df

def train_and_save_model():
    df = prepare_data()
    y = df.pop('result')
    X = df

    # Define and fit the ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), list(X.columns))
        ],
        remainder='passthrough'
    )
    
    X_transformed = preprocessor.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, 'authentication/model.pkl')
    joblib.dump(preprocessor, 'authentication/preprocessor.pkl')

    print("Model and scaler trained and saved.")

if __name__ == "__main__":
    train_and_save_model()
