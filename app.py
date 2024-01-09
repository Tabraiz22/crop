from flask import Flask, render_template, jsonify, request
import pickle
import numpy as np

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

            return render_template('result.html', crop_result=res[0])  # Pass the result to the template
        else:
            return render_template('prediction.html')

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
