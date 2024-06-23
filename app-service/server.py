import os
from flask import Flask, render_template, request, Response
from flask_cors import CORS
import remlaversionutilpy
import requests

from prometheus_client import Counter, generate_latest, start_http_server

REQUEST_COUNTER = Counter('num_requests', 'Number of requests served by the application', ['endpoint'])
PREDICTION_COUNTER = Counter('num_predictions', 'Number of predictions made by the application')


# app-monitoring libraries
import psutil # library to monitor CPU and Memory (monitors computer usage)
# from prometheus_client import Counter, Gauge, Histogram, start_http_server
from threading import Timer

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')

# count_index = 0
# count_predictions = 0 


CORS(app)

model_service_url = os.getenv('MODEL_SERVICE_URL')




@app.route('/')
def index():
    REQUEST_COUNTER.labels(endpoint='/').inc()
    # count_index += 1
    return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
    return f'Version {remlaversionutilpy.VersionUtil.get_version()}'

@app.route('/check-url', methods=['POST'])
def check_url():
    # global count_predictions
    # count_predictions += 1
    PREDICTION_COUNTER.inc()

    json = request.get_json()
    for i in range(10):
        print(model_service_url)
    response = requests.post(model_service_url + "/querymodel", json=json)
    return response.json()

@app.route('/metrics', methods=['GET'])
def metrics():
    # global count_index
    # m = "num_requests{{page=\"index\"}} {}\n".format(count_index)
    # m += "num_predictions {}\n".format(count_predictions) 
    return Response(generate_latest(), mimetype="text/plain")

@app.route('/my_metrics', methods=['POST'])
def post_metrics():
    return f'metrics {count_index}'


if __name__ == '__main__':
    start_http_server(9090)
    app.run(host="0.0.0.0", debug=True, port=8080)
