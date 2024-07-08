import os
import numpy as np
import tensorflow as tf
from keras_preprocessing import image
from keras_applications.vgg16 import preprocess_input
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing import image
from keras._tf_keras.keras.applications.vgg16 import preprocess_input
from keras import backend as K

# Set the image data format explicitly as channel last
K.set_image_data_format('channels_last')

# Define a flask app
app = Flask(__name__)

# Paths to the models
EMBRYO_MODEL_PATH = 'model.resnet101.h5'
SPERM_MODEL_PATH = 'model.VGG16 (1).keras'

# Load your trained models
embryo_model = load_model(EMBRYO_MODEL_PATH)
sperm_model = load_model(SPERM_MODEL_PATH)

print('Models loaded. Check http://127.0.0.1:5000/')

# Function for processing the input image and prediction for sperm
def model_predict_sperm(img_path, model, preprocess_type='default'):
    print("Image path:", img_path)  # Check if the correct file path is received
    # Load the image
    img = image.load_img(img_path, target_size=(224, 224))    #resize to 224x224 pixels shape
    x = image.img_to_array(img)   # change to numpy array

    # Preprocess the image
    if preprocess_type == 'default':
        x = preprocess_input(x)
    elif preprocess_type == 'normalize':
        x = x / 255.0  # Normalize between 0 and 1

    x = np.expand_dims(x, axis=0)     #add axis which is btach size (1,224,224,3)

    print("Processed image shape:", x.shape)  # Print processed image shape for debugging

    y = model.predict(x)
    print("Predictions:", y)  # Print predictions for debugging

    return y[0][0]  # Return the probability of the positive class

# Function for processing the input image and prediction for embryo
def model_predict_embryo(img_path, model):
    print("Image path:", img_path)  # Check if the correct file path is received
    # Preprocessing the image
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    print("Processed image shape:", x.shape)  # Print processed image shape for debugging

    y = model.predict(x)
    print("Predictions:", y)  # Print predictions for debugging

    return y[0][0]  # Return the probability of the positive class

# Home page
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('Home.html')

# about us page
@app.route('/aboutUs', methods=['GET'])
def aboutUs():
    # Main page
    return render_template('About.html')

# contact us page
@app.route('/contact', methods=['GET'])
def contact():
    # Main page
    return render_template('contactPage.html')

# Embryo analysis page
@app.route('/embryo_analysis.html', methods=['GET'])
def embryo_analysis():
     #Embryo analysis page
    return render_template('embryo_analysis.html')

# Sperm analysis page
@app.route('/sperm_analysis.html', methods=['GET'])
def sperm():
    # Sperm analysis page
    return render_template('sperm_analysis.html')

# predict sperm
@app.route('/predict1', methods=['POST'])   #accepts post request
def predict_sperm():
    if request.method == 'POST':    # function will be executed when a post request is sent to /predic1
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)    # directory path of current file
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Determine which model to use based on the referrer
        referrer = request.referrer   # gets URL of page that sent the request
        print(f"Referrer: {referrer}")  # Debug print to check referrer value
        if 'sperm_analysis.html' in referrer:
            model = sperm_model
        elif 'embryo_analysis.html' in referrer:
            model = embryo_model
        else:
            return jsonify({"error": "Invalid analysis type"}), 400

        # Make prediction
        try:
            # Use normalized preprocessing for the final prediction
            raw_prediction = model_predict_sperm(file_path, model, preprocess_type='normalize')

            print(f"Normalized preprocessing prediction: {raw_prediction}")

            # Using default preprocessing for prediction
            pred_class = "Good Sperm" if raw_prediction <= 0.5 else "Bad Sperm"
            if pred_class == "Good Sperm":
                accuracy = float( 1 - raw_prediction)
            else:
                accuracy = float(raw_prediction)

            if pred_class == "Bad Sperm" and accuracy > 0.9999:
                response_data = {
                    "prediction": "Not a sperm.",
                    "accuracy": accuracy
                }
            else:
                response_data = {
                    "prediction": pred_class,
                    "accuracy": accuracy,
                }

            # Return JSON response with prediction and report
            return jsonify(response_data)
        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({"error": "Error during prediction"}), 500

    return None

@app.route('/predict2', methods=['POST'])
def predict_embryo():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Determine which model to use based on the referrer
        referrer = request.referrer
        print(f"Referrer: {referrer}")  # Debug print to check referrer value
        if 'sperm_analysis.html' in referrer:
            model = sperm_model
        elif 'embryo_analysis.html' in referrer:
            model = embryo_model
        else:
            return jsonify({"error": "Invalid analysis type"}), 400

        # Make prediction
        try:
            raw_prediction = model_predict_embryo(file_path, model)
            pred_class = "Good Embryo" if raw_prediction >= 0.5 else "Bad Embryo"

            # Calculate accuracy based on prediction class
            if pred_class == "Good Embryo":
                accuracy = float(raw_prediction)
            else:
                accuracy = float(1 - raw_prediction)

            if pred_class == "Bad Embryo" and accuracy > 0.8:
                response_data = {
                    "prediction": "Not an Embryo.",
                    "accuracy": accuracy ,
                }
            else:
                response_data = {
                    "prediction": pred_class,
                    "accuracy": accuracy,
                }

            # Return JSON response with prediction and report
            return jsonify(response_data)
        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({"error": "Error during prediction"}), 500

    return None

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print(K.backend())
    print(tf.__version__)
