# 🏋️ AI Diet & Workout Recommendation API

A Flask-based REST API that provides personalized **7-day diet plans** and **workout recommendations** for Indian users based on their body metrics, dietary preferences, and fitness goals.

---

## 🚀 Features

- 📊 **Personalized Calorie Calculation** using the Mifflin-St Jeor BMR formula
- 🥗 **7-Day Indian Diet Plan** tailored to Veg / Non-Veg preferences
- 💪 **7-Day Workout Schedule** matched to fitness goals
- 🎯 Supports goals: `Weight Loss`, `Muscle Gain`, `General Fitness`, `Maintenance`
- ⚡ Deployed-ready with `gunicorn` support

---

## 🛠️ Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Backend      | Python, Flask           |
| ML / Data    | Pandas, NumPy, Scikit-learn |
| Server       | Gunicorn                |
| Dataset      | Indian Diet & Workout CSVs |

---

## 📁 Project Structure

```
diet-workout-recommender/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── data/
│   ├── indian_diet_dataset_1000_weight_loss_fitness.csv
│   └── indian_workout_dataset.csv
│
├── models/
│   ├── diet_recommender.py
│   └── workout_recommender.py
│
└── utils/
    └── preprocess.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/AryanKadu/ai_recom_api_strideup.git
cd ai_recom_api_strideup
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python app.py
```

Server runs at `http://localhost:5000`

---

## 📡 API Reference

### `POST /recommend`

Returns a personalized 7-day diet plan and workout schedule.

#### Request Body (JSON)

```json
{
  "age": 22,
  "weight": 70,
  "height": 175,
  "gender": "Male",
  "fitness_goal": "Weight Loss",
  "dietary_preference": "Veg"
}
```

| Field                | Type   | Options                                                  |
|----------------------|--------|----------------------------------------------------------|
| `age`                | float  | Any positive number                                      |
| `weight`             | float  | In kilograms                                             |
| `height`             | float  | In centimeters                                           |
| `gender`             | string | `"Male"` / `"Female"`                                   |
| `fitness_goal`       | string | `"Weight Loss"`, `"Muscle Gain"`, `"General Fitness"`, `"Maintenance"` |
| `dietary_preference` | string | `"Veg"` / `"Non-Veg"`                                   |

#### Response (JSON)

```json
{
  "diet_plan": [
    {
      "Breakfast": { "Food Item": "...", "Calories": 350, ... },
      "Lunch":     { "Food Item": "...", "Calories": 500, ... },
      "Snacks":    { "Food Item": "...", "Calories": 200, ... },
      "Dinner":    { "Food Item": "...", "Calories": 450, ... }
    }
    // ... 7 days
  ],
  "workout_recommendations": [
    {
      "Day": "Day 1",
      "Workout Name": "Running",
      "Workout Type": "Cardio",
      "Target Muscle Group": "Full Body",
      "Calories Burned": 385
    }
    // ... 7 days
  ]
}
```

---

## 🧮 How Calories Are Calculated

Uses the **Mifflin-St Jeor formula**:

- **Male BMR** = `10 × weight + 6.25 × height − 5 × age + 5`
- **Female BMR** = `10 × weight + 6.25 × height − 5 × age − 161`

**TDEE** = `BMR × 1.55` (moderate activity)

| Goal             | Calorie Adjustment |
|------------------|--------------------|
| Weight Loss      | TDEE − 500         |
| Muscle Gain      | TDEE + 300         |
| General Fitness  | TDEE               |
| Maintenance      | TDEE               |

---

## 📦 Deployment

The app uses `gunicorn` for production deployment (e.g., on Railway or Render):

```bash
gunicorn app:app
```

Set the `PORT` environment variable if required by your hosting platform.

---

## 👤 Author

**Aryan Kadu**  
[GitHub](https://github.com/AryanKadu) · PBL Project — StrideUp Platform
