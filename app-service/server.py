import os
from flask import Flask, render_template, request, Response
from flask_cors import CORS
import remlaversionutilpy
import requests


# app-monitoring libraries
import psutil # library to monitor CPU and Memory (monitors computer usage)
# from prometheus_client import Counter, Gauge, Histogram, start_http_server
from threading import Timer

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')
count_index = 0
CORS(app)

model_service_url = os.getenv('MODEL_SERVICE_URL')

# # Prometheus Metrics

# REQUESTS_DAILY = Counter('requests_daily_total', 'Total number of requests per day')
# MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
# CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
# ACTIVE_USERS = Gauge('active_users', 'Number of active users')

# def update_memory_usage():
#     process = psutil.Process()
#     memory_info = process.memory_info()
    # MEMORY_USAGE.set(memory_info.rss)  # Resident Set Size (actual physical memory)

# def update_cpu_usage():
    # CPU_USAGE.set(psutil.cpu_percent(interval=1))  # Get CPU usage percentage over 1 second

@app.route('/')
def index():
    global count_index
    count_index += 1
    return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
    return f'Version {remlaversionutilpy.VersionUtil.get_version()}'

@app.route('/check-url', methods=['POST'])
def check_url():
    json = request.get_json()
    for i in range(10):
        print(model_service_url)
    #response = requests.post(os.getenv('MODEL_SERVICE_URL'), json=json)
    response = requests.post(model_service_url + "/querymodel", json=json)
    return response.json()

@app.route('/metrics', methods=['GET'])
def metrics():
    global count_index
    m += "num_requests{{page=\"index\"}} {}\n".format(count_index)

    return Response(m, mimetype="text/plain")

@app.route('/my_metrics', methods=['POST'])
def post_metrics():
    return f'metrics {count_index}'

# prometheus update time

# Timer(60, update_memory_usage).start()
# Timer(60, update_cpu_usage).start()

# start_http_server(9090)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
