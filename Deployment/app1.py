# Import libraries
import numpy as np
import requests
from flask import Flask, request, jsonify, render_template


import json

API_KEY = "A99STaz2reNjXDvE9j-F9JJ5Xc-v7CL7F0QmFiXJV0kB"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    age =request.form.get('age')
    sex = request.form.get('sex')
    bmi = request.form.get('bmi')
    children = request.form.get('children')
    smoker = request.form.get('smoker')
    region = request.form.get('region')
    

     
    
    print(age)
    print(sex)
    print(bmi)
    print(children)
    print(smoker)
    print(region)
    
    
    data_val = [[age,sex,bmi,children,smoker,region]]

    payload_scoring = {"input_data": [{"fields": [["age","sex","bmi","children","smoker","region"]],
                                       "values": data_val
                                       }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1b1fccd4-3edc-40e7-bb58-14d4a060c71d/predictions?version=2021-10-21', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()

    output = predictions['predictions'][0]['values'][0][0]
  
    predictions = (predictions)
    

    prediction_text = 'premium is predicted to be :'+str(output)
    #print(prediction_text)

    return render_template('index.html', prediction_text=prediction_text)

# Allow the Flask app to launch from the command line
if __name__ == "__main__":
    app.run(debug=True)