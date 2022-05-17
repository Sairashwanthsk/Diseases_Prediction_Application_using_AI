from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory
import joblib
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)

app.secret_key = 'afniemiehfbadsfbverwiroerjeqwtr76rbu30m2hx1h'

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

malaria_model = load_model('model_malaria.h5')

# call model to predict an image
def api_malaria(full_path):
    data = image.load_img(full_path, target_size=(50, 50, 3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255

    #with graph.as_default():
    predicted = malaria_model.predict(data)
    return predicted

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cancer")
def cancer():
    return render_template("cancer.html")

@app.route("/diabetes")
def diabetes():
    #if form.validate_on_submit():
    return render_template("diabetes.html")

@app.route("/heart")
def heart():
    return render_template("heart.html")

@app.route("/liver")
def liver():
    #if form.validate_on_submit():
    return render_template("liver.html")

@app.route("/kidney")
def kidney():
    #if form.validate_on_submit():
    return render_template("kidney.html")

@app.route("/malaria")
def malaria():
    return render_template("malaria.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==8):#Diabetes
        diabetes_model = joblib.load("model_diabetes")
        result = diabetes_model.predict(to_predict)
    elif(size==30):#Cancer
        cancer_model = joblib.load("model_cancer")
        result = cancer_model.predict(to_predict)
    elif(size==12):#Kidney
        kidney_model = joblib.load("model_kidney")
        result = kidney_model.predict(to_predict)
    elif(size==10):
        liver_model = joblib.load("model_liver")
        result = liver_model.predict(to_predict)
    elif(size==11):#Heart
        heart_model = joblib.load("model_heart")
        result = heart_model.predict(to_predict)
    return result[0]

@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if(len(to_predict_list)==30):#Cancer
            result = ValuePredictor(to_predict_list,30)
            disease = 'Breast Cancer'
            route = 'cancer'
        elif(len(to_predict_list)==8):#Daiabtes
            result = ValuePredictor(to_predict_list,8)
            disease = 'Diabetes'
            route = 'diabetes'
        elif(len(to_predict_list)==12):
            result = ValuePredictor(to_predict_list,12)
            disease = 'Kidney Disease'
            route = 'kidney'
        elif(len(to_predict_list)==11):
            result = ValuePredictor(to_predict_list,11)
            disease = 'Heart Disease'
            route = 'heart'
        elif(len(to_predict_list)==10):
            result = ValuePredictor(to_predict_list,10)
            disease = 'Liver Disease'
            route = 'liver'
    if(int(result)==1):
        prediction='Sorry ! Suffering'
    else:
        prediction='Congrats ! you are Healthy' 
    return(render_template("result.html", prediction=prediction, disease=disease, route=route))

# procesing uploaded file and predict it
@app.route('/upload_malaria', methods=['POST','GET'])
def upload_file_malaria():

    if request.method == 'GET':
        return render_template('malaria.html')
    else:
        try:
            file = request.files['image']
            full_name = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(full_name)

            indices = {0: 'PARASITIC', 1: 'Uninfected'}
            result = api_malaria(full_name)
            print(result)

            predicted_class = np.asscalar(np.argmax(result, axis=1))
            accuracy = round(result[0][predicted_class] * 100, 2)
            label = indices[predicted_class]
            return render_template('predict_malaria.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        except Exception as e:
            flash(str(e), "danger")      
            return redirect(url_for("malaria"))

if __name__ == '__main__':
    app.run(debug=True)