from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load model and scaler
model = joblib.load("diabetes_model.joblib")
scaler = joblib.load("scaler.joblib")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_features = [float(request.form.get(feature)) for feature in [
            'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
        ]]
        features_scaled = scaler.transform([input_features])
        prediction = model.predict(features_scaled)[0]
        result = "Diabetic" if prediction == 1 else "Not Diabetic"
        return render_template('index.html', prediction=result)
    except:
        return render_template('index.html', prediction="Invalid Input")


if __name__ == "__main__":
    from os import environ
    app.run(debug=False, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
