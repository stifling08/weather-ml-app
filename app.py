from flask import Flask, request, render_template
import pickle
import numpy as np
import time

app = Flask(__name__)

weather_classes = ['clear', 'cloudy', 'drizzly', 'foggy', 'hazey', 'misty', 'rain', 'smokey', 'thunderstorm']

# Load the trained weather prediction model
def load_model(model_path='model/model.pkl'):
    with open(model_path, 'rb') as model_file:
        return pickle.load(model_file)


# Classify weather using the trained machine learning model
def classify_weather(features):
    model = load_model()

    start = time.time()

    prediction_index = int(model.predict(features)[0])

    latency = round((time.time() - start) * 1000, 2)

    # Return the actual prediction from the model
    prediction = weather_classes[prediction_index]

    return prediction, latency


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Convert submitted weather measurements into numbers
            temperature = float(request.form['temperature'])
            pressure = float(request.form['pressure'])
            humidity = float(request.form['humidity'])
            wind_speed = float(request.form['wind_speed'])
            wind_deg = float(request.form['wind_deg'])

            rain_1h = float(request.form.get('rain_1h', 0) or 0)
            rain_3h = float(request.form.get('rain_3h', 0) or 0)
            snow = float(request.form.get('snow', 0) or 0)
            clouds = float(request.form.get('clouds', 0) or 0)

            # Combine measurements into the model input
            features = np.array([
                temperature, pressure, humidity,
                wind_speed, wind_deg, rain_1h,
                rain_3h, snow, clouds
            ]).reshape(1, -1)

            # Generate the weather prediction
            prediction, latency = classify_weather(features)

            return render_template(
                'result.html',
                prediction=prediction,
                latency=latency
            )

        except Exception as e:
            error_msg = f"Error processing input: {e}"
            return render_template('form.html', error=error_msg)

    # Display the weather input form
    return render_template('form.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
