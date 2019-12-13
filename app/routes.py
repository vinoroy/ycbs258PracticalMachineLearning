from flask import render_template
from app import app
from app.forms import LabForm

from flask import render_template, flash, redirect

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
import googleapiclient.discovery

import sys
import os


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/prediction', methods=['GET', 'POST'])
def lab():
    form = LabForm()

    if form.validate_on_submit():

        # get the dorm data for the patient data and put into a form for the
        X_test = np.array([[float(form.preg.data),float(form.glucose.data),float(form.blood.data),float(form.skin.data),float(form.insulin.data),float(form.bmi.data),float(form.dpf.data),float(form.age.data)]])
        print(X_test.shape)
        print(X_test)

        # in order to make a prediction we must scale the data using the same scale as the one used to make
        # model

        # get the data for the diabetes data.
        data = pd.read_csv('./diabetes.csv', sep=',')

        # extract the X and y from the imported data
        X = data.values[:, 0:8]
        y = data.values[:, 8]

        # use MinMaxScaler to fit a scaler object
        scaler = MinMaxScaler()
        scaler.fit(X)

        # min max scale the data for the prediction
        X_test = scaler.transform(X_test)

        # create the resource to the model web api on GCP
        MODEL_NAME = "my_pima_model2"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sapient-pen-260901-dc0c62411b24.json"
        project_id = 'sapient-pen-260901'
        model_id = MODEL_NAME
        model_path = "projects/{}/models/{}".format(project_id, model_id)
        model_path += "/versions/v0001/"  # if you want to run a specific version
        ml_resource = googleapiclient.discovery.build("ml", "v1").projects()


        # format the data as a json to send to the web api
        input_data_json = {"signature_name": "serving_default",
                           "instances": X_test.tolist()}
        # make the prediction
        request = ml_resource.predict(name=model_path, body=input_data_json)
        response = request.execute()
        if "error" in response:
            raise RuntimeError(response["error"])

        # extract the prediction from the response
        predD =  np.array([pred['dense_5'] for pred in response["predictions"]])
        print(predD[0][0])
        res = predD[0][0]

        return render_template('result.html',res=res)

    return render_template('prediction.html', form=form)





