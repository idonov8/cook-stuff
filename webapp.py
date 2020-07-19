from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from clarifai.rest import ClarifaiApp, Image as ClImage
from werkzeug.utils import secure_filename

load_dotenv()
SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")
CLARIFAI_KEY = os.getenv("CLARIFAI_KEY")
UPLOAD_FOLDER = 'static/Pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

clarifai_app = ClarifaiApp(api_key=CLARIFAI_KEY)
model = clarifai_app.models.get('food-items-v1.0')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getRecipe', methods=['POST'])
def getRecipe():

    # Handle image file
    if 'image' not in request.files:
        print("did not recive a file")
        pass # TODO: handle error
    file = request.files['image']
    if file.filename == '':
            pass # TODO: handle 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        pass # TODO: handle error

    # A call to clarifai
    image = ClImage(filename=UPLOAD_FOLDER+'/'+ filename)
    prediction = model.predict([image])
    ingredients = []
    print(prediction)
    for ingredient in prediction['outputs'][0]['data']['concepts']:
        ingredients.append(ingredient['name'])


    #ingredients = request.form['ingredients']

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