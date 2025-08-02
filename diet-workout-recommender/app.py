from flask import Flask, request, jsonify
from utils.preprocess import preprocess_diet_data, preprocess_workout_data
from models.diet_recommender import recommend_diet
from models.workout_recommender import recommend_workout

app = Flask(__name__)

# Preprocess data
diet_data = preprocess_diet_data(r"C:\Users\Humanshu\Desktop\PBL\diet-workout-recommender\data\indian_diet_dataset_1000_weight_loss_fitness.csv")
workout_data = preprocess_workout_data(r"C:\Users\Humanshu\Desktop\PBL\diet-workout-recommender\data\indian_workout_dataset.csv")

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input from the request
    user_input = request.json
    
    # Map user input to model input
    user_input['calories'] = 2000  # Example calorie requirement
    user_input['category'] = 1 if user_input['dietary_preference'] == "Veg" else 0
    user_input['calories_burned'] = 400  # Example calories burned
    
    # Filter diet data based on user preferences
    filtered_diet_data = diet_data[
        (diet_data['Veg/Non-Veg'] == 'Veg') | 
        ((diet_data['Veg/Non-Veg'] == 'Non-Veg') & (user_input['dietary_preference'] == "Non-Veg"))
    ]
    filtered_diet_data = filtered_diet_data[filtered_diet_data['Cheat Meal'] == "No"]  # Exclude cheat meals
    
    # Get recommendations
    diet_recommendations = recommend_diet(user_input, filtered_diet_data)
    workout_recommendations = recommend_workout(user_input, workout_data)
    
    # Generate a 7-day diet plan
    diet_plan = []
    meal_types = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']

    # Create a copy of the filtered diet data to track used meals
    available_diet_data = diet_recommendations.copy()

    for day in range(7):
        day_plan = {}
        for meal in meal_types:
            # Filter meals for the current meal type
            meal_recommendations = available_diet_data[available_diet_data['Meal Type'] == meal]
            
            if not meal_recommendations.empty:
                # Randomly select one meal for the current meal type
                selected_meal = meal_recommendations.sample(1)
                day_plan[meal] = selected_meal.to_dict(orient='records')[0]
                
                # Remove the selected meal from the available data to avoid repetition
                available_diet_data = available_diet_data.drop(selected_meal.index)
            else:
                # If no meals are available for the current meal type, fallback to the original dataset
                fallback_meal_recommendations = filtered_diet_data[filtered_diet_data['Meal Type'] == meal]
                if not fallback_meal_recommendations.empty:
                    # Randomly select one meal from the fallback dataset
                    selected_meal = fallback_meal_recommendations.sample(1)
                    day_plan[meal] = selected_meal.to_dict(orient='records')[0]
                else:
                    # If no fallback meals are available, leave it empty
                    day_plan[meal] = {"Error": f"No meal available for {meal}"}
        diet_plan.append(day_plan)
    
    # Convert recommendations to JSON
    response = {
        "diet_plan": diet_plan,
        "workout_recommendations": [
        {
            "Day": f"Day {day + 1}",
            "Workout Name": workout.get("Workout Name", "Unknown"),
            "Workout Type": workout.get("Workout Type", "Unknown"),
            "Target Muscle Group": workout.get("Target Muscle Group", "Unknown"),
            "Calories Burned": workout.get("Calories Burned", 0)
        }
        for day, workout in enumerate(workout_recommendations.to_dict(orient='records')[:7])
     ]
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)