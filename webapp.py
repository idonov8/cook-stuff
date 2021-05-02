from flask import Flask, render_template, request, jsonify, session as login_session, flash, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from db.models import *
from db.database import session
from datetime import datetime
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

load_dotenv()
SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")
CLARIFAI_KEY = os.getenv("CLARIFAI_KEY")
MANAGER_PASS = os.getenv("MANAGER_PASS")

UPLOAD_FOLDER = 'static/Pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
metadata = (('authorization', 'Key '+ CLARIFAI_KEY),)

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
        imageURL = UPLOAD_FOLDER+'/'+ filename
        with open(imageURL, "rb") as f:
            file_bytes = f.read()

        print(imageURL)
        APIrequest = service_pb2.PostModelOutputsRequest(
            model_id='bd367be194cf45149e75f01d59f77ba7',
            inputs=[
                resources_pb2.Input(data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                ))
            ]
        )
        response = stub.PostModelOutputs(APIrequest, metadata=metadata)

        if response.status.code != status_code_pb2.SUCCESS:
            raise Exception("Request failed, status code: " + str(response.status.code))

        for ingredient in response.outputs[0].data.concepts:
            print('%12s: %.2f' % (ingredient.name, ingredient.value))
            ingredients.append(ingredient.name)

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
        return jsonify(recipes=results, ingredients=ingredients)

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
    if 'admin' in login_session:
        del login_session['admin']
    return redirect(url_for('manager'))

@app.route('/sendFeedback',  methods=['POST'])
def sendFeedback():
    date = datetime.today()
    name = request.form['name']
    content = request.form['content']
    if name and content:
        session.add(Feedback(date=date, name=name, content=content))
        session.commit()
        return jsonify(success='Feedback sent!')
    else: 
        return jsonify(error="Missing argument")

@app.route('/manager/delete/<int:id>', methods=['DELETE'])
def deleteFeedback(id):
    session.query(Feedback).filter_by(id=id).delete()
    session.commit()
    return jsonify(success='feedback deleted!')

if __name__ == '__main__':
    app.run(debug=True)