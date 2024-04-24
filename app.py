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
def index():
    return render_template('index.html')

@app.route("/wellbeing")
def wellbeing():
    return render_template('wellbeing.html')

@app.route("/lifestyle")
def lifestyle():
    return render_template('lifestyle.html')

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/symptoms")
def symptoms():
    return render_template('symptoms.html')

@app.route("/cause")
def cause():
    return render_template('Cause.html')


@app.route("/reasons")
def reason():
    return render_template('reasons.html')


@app.route("/food")
def food():
    return render_template('food.html')

@app.route("/form")
def form():
    return render_template('form.html')


@app.route("/diet20")
def diet20():
    return render_template('0-20_diet.html')

@app.route("/exercise20")
def exercise20():
    return render_template('0-20_exercise.html')


@app.route("/diet40")
def diet40():
    return render_template('20-40_diet.html')

@app.route("/exercise40")
def exercise40():
    return render_template('20-40_exercise.html')

@app.route("/diet60")
def diet60():
    return render_template('40-60_diet.html')

@app.route("/exercise60")
def exercise60():
    return render_template('40-60_exercise.html')


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
    diabetes = 1 if request.form.get('diabetesY') == 'on' else 0; 
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
    
    formatted_probability = float("{:.3f}".format(probabilities[0] * 100))


    

    if formatted_probability > 0 and formatted_probability <= 20:
        return render_template('0-20.html', pred=formatted_probability, string = "Case 1")
    elif formatted_probability > 20 and formatted_probability <= 40:
         return render_template('20-40.html', pred=formatted_probability, string = "Case 2")
    elif formatted_probability > 40 and formatted_probability <= 60:
         return render_template('40-60.html', pred=formatted_probability, string = "Case 3")
    elif formatted_probability > 60 and formatted_probability <= 80:
         return render_template('60-80.html', pred=formatted_probability, string = "Case 4")
    else:
        return render_template('80-100.html', pred=formatted_probability, string = "Aap marne wale ho")
    
    


    

if __name__ == "__main__":
    app.run(debug=True)
