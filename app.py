from flask import Flask, render_template, request
import joblib
import numpy as np
from scipy import optimize

app = Flask(__name__)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def predict_probabilities(X, theta):
    return sigmoid(np.dot(X, theta))

@app.route("/")
def hello():
    return render_template('form.html')

@app.route("/predict", methods=['POST'])
def HeartDiseasePrediction():

   
    gender = 1 if request.form.get('genderM') == 'on' else 0
    age = int(request.form.get('age'))
    if ( request.form.get('eduP') == 'on' or request.form.get('eduN') == 'on' ):
        education = 1
    elif ( request.form.get('eduTenth') == 'on'):
        education = 2
    elif ( request.form.get('eduT') == 'on'):
        education = 3
    elif ( request.form.get('eduPost') == 'on'  or  request.form.get('eduU') == 'on' ):
        education = 4
    else:
        education = 1
    
    daily_smoker = 1 if request.form.get('smokerY') == 'on' else 0
    cigs_per_day = int(request.form.get('cigs'))
    blood_pressure_medication = 1 if request.form.get('bpmedY') == 'on' else 0
    stroke_prevalent = 1 if request.form.get('strokeY') == 'on' else 0
    hypertension = 1 if request.form.get('hyperY') == 'on' else 0
    diabetes = 0; #temp value until it is included in the form
    cholestrol = int(request.form.get('chol'))
    systolic_bp = int(request.form.get('sysbp'))
    diastolic_bp = int(request.form.get('diabp'))
    bmi = float(request.form.get('bmi'))
    heart_rate = int(request.form.get('heartrate'))
    glucose = int(request.form.get('glucose'))

    
    X = np.array([[gender , age , education, daily_smoker,cigs_per_day ,blood_pressure_medication,stroke_prevalent, hypertension, diabetes, cholestrol, systolic_bp, diastolic_bp,bmi, heart_rate, glucose ]])
    # Load the model
    X = np.concatenate([np.ones((X.shape[0], 1)), X], axis=1)
    model = joblib.load('logistic_regression_model.pkl')
    # Retrieve the optimized parameters
    theta = model['x']
    # Compute the probabilities
    probabilities = predict_probabilities(X, theta)
    
    # Print the predicted probability
    print('Predicted probability:', probabilities[0])
    
    formatted_probability = "{:.3f}".format(probabilities[0] * 100)
    return render_template('after.html', pred=formatted_probability)

    

if __name__ == "__main__":
    app.run(debug=True)
