def get_user_input():
    print("Enter your details:")
    age = int(input("Age: "))
    gender = input("Gender (Male/Female): ")
    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))
    fitness_goal = input("Fitness Goal (Weight Loss/Muscle Gain/General Fitness): ")
    dietary_preference = input("Dietary Preference (Veg/Non-Veg): ")
    return {
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "fitness_goal": fitness_goal,
        "dietary_preference": dietary_preference
    }