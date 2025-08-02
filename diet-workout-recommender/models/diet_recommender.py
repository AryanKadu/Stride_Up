from sklearn.neighbors import NearestNeighbors
import pandas as pd

def recommend_diet(user_input, diet_data):
    """
    Recommends meals based on user input using the Nearest Neighbors algorithm.

    Args:
        user_input (dict): A dictionary containing user preferences like calories and category.
        diet_data (pd.DataFrame): The dataset containing meal information.

    Returns:
        pd.DataFrame: A DataFrame containing the recommended meals.
    """
    # Ensure the dataset has the required columns
    required_columns = ['Calories (kcal)', 'Category']
    if not all(col in diet_data.columns for col in required_columns):
        raise ValueError(f"The dataset must contain the following columns: {required_columns}")

    # Prepare the model
    model = NearestNeighbors(n_neighbors=5, metric='cosine')
    model.fit(diet_data[['Calories (kcal)', 'Category']])

    # Create a user vector for recommendation
    user_vector = [[user_input['calories'], user_input['category']]]

    # Get the nearest neighbors
    distances, indices = model.kneighbors(user_vector)

    # Return the recommended meals
    return diet_data.iloc[indices[0]].reset_index(drop=True)