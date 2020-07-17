from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()
SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getRecipe', methods=['POST'])
def getRecipe():
    # A call to clarifai
    ingredients = request.form['ingredients']

    # Get recipe from spoonacular
    if ingredients:
        payload = {
            'fillIngredients': False,
            'ingredients': ingredients,
            'limitLicense': False,
            'number': 5,
            'ranking': 1
        }
        endpoint='https://api.spoonacular.com/recipes/findByIngredients?apiKey='+SPOONACULAR_KEY

        r = requests.get(endpoint, params=payload)
        results = r.json() 
        title = results[0]['title']
        print(title)
        return jsonify(recipes=results)

    print('error lol')
    return jsonify(error="No ingredients were supplied!")



if __name__ == '__main__':
    app.run(debug=True)