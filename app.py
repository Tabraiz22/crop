from flask import Flask, render_template, jsonify, request
import pickle
import numpy as np
import sqlite3
from flask import redirect, url_for


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    try:
        if request.method == 'POST':
            nitro = request.form.get('nitrogen')
            phos = request.form.get('phosphorus')
            kp = request.form.get('potassium')
            temp = request.form.get('temperature')
            hum = request.form.get('humidity')
            ph = request.form.get('ph')
            rain = request.form.get('rainfall')

            print(nitro, phos, kp, temp, hum, ph, rain)

            with open('model.pkl', 'rb') as model_file:
                mlmodel = pickle.load(model_file)

            input_data = np.array([[float(nitro), float(phos), float(kp), float(temp), float(hum), float(ph), float(rain)]])
            res = mlmodel.predict(input_data).tolist()  # Convert to list
            conn = sqlite3.connect('cropdata.db')
            cur =conn.cursor()
            cur.execute(f'''INSERT INTO CROP VALUES({nitro},{phos},{kp},{temp},{hum},{ph},{rain},'{res[0]}')''')
            conn.commit()
            return render_template('result.html', crop_result=res[0])  # Pass the result to the template
        else:
            return render_template('prediction.html')

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/showdata', methods=['GET', 'POST'])    
def showdata():
    try:
        conn = sqlite3.connect('cropdata.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM CROP")
        data = cur.fetchall()
        
        # Fetch the predicted data (you may need to modify this based on your model)
        predicted_data = []
        with open('model.pkl', 'rb') as model_file:
            mlmodel = pickle.load(model_file)
            for row in data:
                input_data = np.array([row[:7]])  # Assuming the first 7 columns are the input features
                predicted_result = mlmodel.predict(input_data).tolist()
                predicted_data.append(predicted_result[0])

        conn.close()
        return render_template('showdata.html', data=data, predicted_data=predicted_data)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)                             
