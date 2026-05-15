import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

BASE_DIR = os.path.dirname(__file__)

data = pd.read_csv(os.path.join(BASE_DIR, "career_data.csv"))

X = data[['interest', 'skills', 'aptitude', 'personality', 'work']]
y = data['career']

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, os.path.join(BASE_DIR, "career_model.pkl"))

print("Model trained successfully")
