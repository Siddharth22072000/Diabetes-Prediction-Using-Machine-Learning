from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model = pickle.load(open('ensemble_model.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request.
    Gender = request.form.get('gender').lower()
    if Gender=="female":
        Gender=0
    elif Gender=="male":
        Gender=1

    Age = float(request.form.get('age'))
    Hypertension = int(request.form.get('hypertension'))
    HeartDisease = int(request.form.get('heartdisease'))
    SmokingHistory = request.form.get('smokinghistory').lower()
    if SmokingHistory=="formerly smoked":
        SmokingHistory=0
    elif SmokingHistory=="never smoked":
        SmokingHistory=1
    elif SmokingHistory=="smokes":
        SmokingHistory=2
    elif SmokingHistory=="unknown":
        SmokingHistory=3
    else:
        SmokingHistory=4
    BMI = float(request.form.get('bmi'))
    HbA1clevel = float(request.form.get('HbA1clevel'))
    BloodGlucoseLevel = int(request.form.get('bloodglucoselevel'))

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict([np.array([Gender,Age, Hypertension, HeartDisease, SmokingHistory, BMI,
                                           HbA1clevel, BloodGlucoseLevel])])

    # The prediction result will be returned to the UI.
    if prediction[0]==0:
        output = 'Not Likely to be Diabetic'
    elif prediction[0]==1:
        output = 'Very Likely to be Diabetic'

    return render_template('index.html', prediction=output)  
    

if __name__ == '__main__':
    #
    app.run(port=5000, debug=True)