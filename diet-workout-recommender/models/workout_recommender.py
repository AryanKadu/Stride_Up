from sklearn.neighbors import NearestNeighbors

def recommend_workout(user_input, workout_data):
    model = NearestNeighbors(n_neighbors=5, metric='cosine')
    model.fit(workout_data[['Calories Burned', 'Category']])
    
    # Example user input for recommendation
    user_vector = [[user_input['calories_burned'], user_input['category']]]
    distances, indices = model.kneighbors(user_vector)
    return workout_data.iloc[indices[0]]