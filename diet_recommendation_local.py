def recommend_diet(age, gender, weight, height, activity_level, goal):
    # BMR
    if gender.lower() == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161
    
    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    tdee = bmr * activity_factors.get(activity_level.lower(), 1.2)

    if goal.lower() == "weight loss":
        tdee -= 500
    elif goal.lower() == "weight gain":
        tdee += 500

    # Macronutrients
    if age < 18:
        macro_split = {"protein":0.25,"carbs":0.55,"fat":0.2}
    elif age <= 50:
        if goal.lower() == "weight loss":
            macro_split = {"protein":0.3,"carbs":0.4,"fat":0.3}
        elif goal.lower() == "weight gain":
            macro_split = {"protein":0.2,"carbs":0.55,"fat":0.25}
        else:
            macro_split = {"protein":0.25,"carbs":0.5,"fat":0.25}
    else:
        macro_split = {"protein":0.3,"carbs":0.45,"fat":0.25}

    protein_g = (tdee*macro_split["protein"])/4
    carbs_g = (tdee*macro_split["carbs"])/4
    fat_g = (tdee*macro_split["fat"])/9

    bmi = weight/((height/100)**2)
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Normal weight"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    return {
        "calories": int(tdee),
        "protein_g": round(protein_g,1),
        "carbs_g": round(carbs_g,1),
        "fat_g": round(fat_g,1),
        "bmi": round(bmi,1),
        "bmi_status": bmi_status
    }
