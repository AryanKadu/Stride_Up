import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_diet_data(file_path):
    diet_data = pd.read_csv(file_path)
    diet_data['Calories (kcal)'] = StandardScaler().fit_transform(diet_data[['Calories (kcal)']])
    diet_data['Category'] = LabelEncoder().fit_transform(diet_data['Category'])
    return diet_data

def preprocess_workout_data(file_path):
    workout_data = pd.read_csv(file_path)
    workout_data['Calories Burned'] = StandardScaler().fit_transform(workout_data[['Calories Burned']])
    workout_data['Category'] = LabelEncoder().fit_transform(workout_data['Category'])
    return workout_data