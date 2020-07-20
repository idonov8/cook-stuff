from flask import Flask, render_template, request, jsonify, session as login_session, flash, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from clarifai.rest import ClarifaiApp, Image as ClImage
from werkzeug.utils import secure_filename
from db.models import *
from db.database import session

load_dotenv()
SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")
CLARIFAI_KEY = os.getenv("CLARIFAI_KEY")
MANAGER_PASS = os.getenv("MANAGER_PASS")

UPLOAD_FOLDER = 'static/Pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

clarifai_app = ClarifaiApp(api_key=CLARIFAI_KEY)
model = clarifai_app.models.get('food-items-v1.0')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'not_so_secret'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getRecipe', methods=['POST'])
def getRecipe():
    ingredients = []
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

        # A call to clarifai
        image = ClImage(filename=UPLOAD_FOLDER+'/'+ filename)
        prediction = model.predict([image])
        print(prediction)
        for ingredient in prediction['outputs'][0]['data']['concepts']:
            ingredients.append(ingredient['name'])

        # TODO: add delete file after use
    else:
        pass # TODO: handle error



    ingredients.append(request.form['ingredients'])

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

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    error=None
    if request.method=='POST':
        password = request.form['password']
        if password == MANAGER_PASS:
            login_session['admin'] = True
            feedbacks = session.query(Feedback).all()
            return render_template('feedbackView.html', feedbacks=feedbacks)
        else:
            error = 'Wrong Password'
    if 'admin' in login_session:
        feedbacks = session.query(Feedback).all()
        return render_template('feedbackView.html', feedbacks=feedbacks)
    return render_template('managerLogin.html', error=error)

@app.route('/manager/logout')
def logout():
    del login_session['admin']
    return redirect(url_for('manager'))

if __name__ == '__main__':
    app.run(debug=True)