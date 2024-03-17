# To install requests - pip3 install requests
import requests
import numpy as np
import json
import pandas as pd
import random
import re


## Setting up API Keys 
#Go to these Links
api_ninjas_link = "https://api-ninjas.com/register"
calorieninja = "https://calorieninjas.com/register"


# 1. Once signed up then you can login and go to Account
# 2. Scroll down until you see API Key section
# 3. Click Show API key and copy API key

def get_recipes(query, mode):
    # Get the recipes
    if mode == 'recipes':
        api_url = "https://api.api-ninjas.com/v1/recipe"
        headers = { 
        "X-API-Key": "Enter api_ninjas API"
    }

    # Get Ingredient Information   
    elif mode == 'ingredients':
        api_url = 'https://api.calorieninjas.com/v1/nutrition'
        headers = {
           'X-Api-Key':'Enter CalorieNinjas API'
        }

    querystring = {"query": query}
    response = requests.get(api_url, headers = headers, params = querystring)
    return response.json()

def make_workout_plan(intensity_option, type_option):
    default = ['cardio','olympic_weightlifting','plyometrics','powerlifting','strength',
                'stretching','strongman']
    

    if type_option not in default:
        name = type_option
        type_option = None

    if type_option == None:
        querystring = {"name":name, 'difficulty': intensity_option} 
    else:
        querystring = {"type":type_option, "difficulty":intensity_option}


    print(querystring)
    url = "https://api.api-ninjas.com/v1/exercises"
    headers = {"X-API-Key": "Enter api_ninja API",}
    response = requests.get(url, headers=headers, params=querystring)

    return response.json()





# Query 1: Ask whether they would like to plan an their diet or excercise
def get_json(file):
    #Funtion to read json files
    with open(file, 'r') as f:
        # Load the JSON data into a Python dictionary
        data = json.load(f)

    return data


def save_json(data, filename):
    #Funtion to save json file
    print("\n Saving your results now...")
    with open(filename, 'w') as f:
        json.dump(data, f, indent = 2)


def get_input():
    create_plan = input('Would you like to plan your 🍊 diet or 🚲 exercise? \nAnswer: ')

    create_plan = create_plan.lower()

    # Check other option as users may wwant to use something different
    nutrition = ['food', 'diet', 'nutrition', 'recipe', 'calories', '🍊']
    exercise = ['activity', 'conditioning', 'training', 'workout', 'body', 'exercise', '🚲 ']

    # Simplify create_plan into a nyumerical output
    if create_plan in nutrition:
        get_nutrition()
    elif create_plan in exercise:
        get_excercise()
    else:
        print("Sorry that input isn't valid. Please select diet or exercise.")
        # Will give the user another opportunity to select the necessary option
        create_plan = get_input()

    return create_plan



def check_option(input_data, mode = None, tries = 3):
    # Check each of the options to ensure they are valid
    if mode == 'intensity':
        #Creates a list with numbers ranging from 1 to 10
        if int(input_data) > 0 and int(input_data) < 11:
            selected_type = True
            input_data = int(input_data)

            # Categorises the intensity level from 1- 10 to level of difficulty
            if input_data <= 3:
                input_data =  'beginner'
            elif input_data > 3 and input_data <=6:
                input_data = "intermediate"
            elif input_data > 6 and input_data <= 10:
                input_data = "expert"
        else:
            #Allows user three tries before selecting beginner
            while input_data > 0 and input_data < 11:
                if tries >0: 
                    print("Sorry, we don't recognise that entry. Please try again")
                    intensity_option = input('On a scale from 1 - 10, how difficult 🥵 would you like your workout to be? \nSelect Intensity: : ')
                    tries -= 1
                else:
                    input_data = 'beginner'

    elif mode == 'type':
        # Check to make sure a valid entry is entered
        input_data = int(input_data)
        activity_type =  activity_type = {0:'Random', 1:'cardio', 2:'weightlifting', 3:'plyometrics [jump_training]', 4:'strength', 5:'stretching', 6:'powerlifting'}
        if input_data  >= 0 and input_data < 7:
            selected_exercise = True
            
        else:
            while input_data >= 0 and input_data < 8:
                if tries > 0: 
                    print("Please select one of these options: ")
                    for key, value in activity_type.items():
                        print(f' {key}: {value}')
                    input_data = input("Select The Number of the Workout You Would like: \nSelect Exercise Type:")
                    input_data = int(input_data) 
                    tries -= 1              
                else:
                    input_data = 0

        # select a random type if none selected.
        if input_data == 0: 
                print("Selecting Random Exercise Type...")
                input_data = np.random.randint(1, 7)  # Generate a random integer between 1 and 6 (inclusive)

        activity = activity_type[input_data]
        input_data = activity


    return input_data




    
def get_excercise(intensity_option = None, muscle_groups = None, type_option = None):
    #Parameters for acitvity type
    activity_type = {0:'Random', 1:'cardio', 2:'weightlifting', 3:'plyometrics', 4:'strength', 5:'stretching',6:'powerlifting'}
  
    print(" \nGreat! Let's create an exercise plan! \n")
    print("Let's make an exercise plan that fits your needs. \n")
    print("Feel free to press enter if you want a random selection of exercises \n")

    #Get intensity type based on scale
    intensity_option = int(input('On a scale from 1 - 10, how difficult 🥵 would you like your workout to be? \nSelect Intensity: '))
    intensity_option = check_option(intensity_option, mode ='intensity')
    
    print(f"\n Great, we will search for exercises with {intensity_option} intensity \n")
    print("There are lots of excercise to choose from: \n")

    for key, value in activity_type.items():
        print(f' {key}: {value}')
    print("\n")

    #Select type of workout 
    type_option = input("Select The Number of the Workout You Would like: \nExercise Type:")
    type_option = check_option(type_option, mode = 'type')

    print(f" \nGreat! Looks like you want to focus on {type_option}")


    print("Curating your workout plan ... \n\n")
    workout = make_workout_plan(intensity_option=intensity_option, type_option=type_option)

    workout = save_json(workout, 'exercise_plan.json')
    print('Your workout has been saved')


## Option 2: Get nutrition recipe

def calculate_calories(data, serving_size):
    total_calories, total_protein, total_fat_total_g = 0, 0, 0
    total_fat_saturated, sodium_mg, potassium_mg = 0,0,0
    carbohydrates_total_g, cholesterol_mg, fiber_g, sugar_g = 0,0,0,0
    #Iterate over each dictionary in the 'items' list
    for item in data['items']:
        # Add the numerical values to the totals
        total_calories += item['calories']
        total_protein += item['protein_g']
        total_fat_total_g += item['fat_total_g']
        total_fat_saturated += item['fat_saturated_g']
        sodium_mg += item['sodium_mg']
        potassium_mg += item['potassium_mg']
        carbohydrates_total_g += item['carbohydrates_total_g']
        cholesterol_mg += item['cholesterol_mg']
        fiber_g += item['fiber_g']
        sugar_g += item['sugar_g']

    # Print the total values
    spec_list = [total_calories, total_protein, total_fat_total_g, total_fat_saturated, sodium_mg, potassium_mg, carbohydrates_total_g, cholesterol_mg, fiber_g, sugar_g]
    keys = ['calories', 'protein_g', 'fat_total_g', 'fat_saturated', 'sodium_mg', 'potatassium_mg', 'carbohydrates_total_g', 'cholesterol_mg', 'fiber_g', 'sugar_g']
    nutrition_dict = {keys[i]: float(spec_list[i]/serving_size) for i in range(len(spec_list))}
   
    return nutrition_dict

def get_nutrition():
    print("Great, Let's get some recipe ideas! \n")
    search = input('What type of food would you like to eat? \nI want to eat: ')
    print("\n Great!, Let's find some healthy recipes.")
    print("\n Adults should eat between 500 - 700 calories per afternoon meal \n")
    print("Let's find a healthy meal to cook tonight! \n")
    response = get_recipes(search, mode= 'recipes')
    
    print('Recipes Found: ')
    top_three = []
    for i in range(5):
        select_response = response[i]
        ingredients = select_response['ingredients']
        title = select_response['title']
        serving_size = int(select_response['servings'].split(' ')[0])
        full_ingredients = []

        #Split Ingredients 
        ingredients = ingredients.split('|')
        for ingredient in ingredients: 
            ingredient = ingredient.split(';')[0]
            ingredient = ingredient.replace(' c ', ' cup ')
            ingredient = ingredient.replace(' tb ', ' tbsp ')
            ingredient = ingredient.replace(' lg ', ' Large ')
            ingredient = ingredient.replace(' ts ', ' tsp ')
            ingredient = ingredient.replace(' 1/2 ', '.5 ')
            ingredient = ingredient.split(' or ') [-1]
            #json_input = get_recipes(ingredient, mode='ingredients')
            full_ingredients.append(ingredient)
        query_string = ', '.join(full_ingredients)
        check_calories = get_recipes(query_string, mode='ingredients')
        #print(check_calories)
        saved_dict = calculate_calories(check_calories, serving_size)
    
        # Only save the healthier recipes <= 800 calories
        if saved_dict['calories'] <= 800:
            print('Recipe Name: ', title)
            select_response['Ingredients Info'] = check_calories
            select_response['Nutritional Information'] = saved_dict
            top_three.append(select_response)

    save_json(top_three, "recipes_v1.json")

get_input()

    