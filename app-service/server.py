import datetime
import os
from threading import Timer
import time
import numpy as np
from flask import Flask, render_template, request, Response
from flask_cors import CORS
import remlaversionutilpy
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../app-frontend/templates', static_folder='../app-frontend/static')
CORS(app)

url_check_count = 0
visit_count_today = 0
response_times = []

histogram_buckets = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
histogram_data = { bucket: 0 for bucket in histogram_buckets }
histogram_data['+Inf'] = 0

def reset_daily_count():
    global daily_visit_count
    daily_visit_count = 0
    
    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=0, minute=0, second=0, microsecond=0)
    delta_t = y - x
    secs = delta_t.total_seconds()

    t = Timer(secs, reset_daily_count)
    t.start()

@app.route('/')
def index():
    global visit_count_today
    visit_count_today += 1

    return render_template('index.html')

@app.route('/version', methods=['GET'])
def version():
    return f'Version {remlaversionutilpy.VersionUtil.get_version()}'

@app.route('/check-url', methods=['POST'])
def check_url():
    start_time = time.time()
    
    global url_check_count
    url_check_count += 1

    json = request.get_json()
    response = requests.post(os.getenv('MODEL_SERVICE_URL') + '/querymodel', json=json)

    duration = time.time() - start_time
    response_times.append(duration)

    for bucket in histogram_buckets:
        if duration <= bucket:
            histogram_data[bucket] += 1
            break
    else:
        histogram_data['+Inf'] += 1

    return response.json()

@app.route('/metrics', methods=['GET'])
def metrics():
    global url_check_count, visit_count_today, histogram_data, response_times

    quantiles = np.percentile(response_times, [50, 90, 99]) if response_times else [0, 0, 0]

    m = "#HELP url_check_count The total number of URL checks\n"
    m += "#TYPE url_check_count counter\n"
    m += f"url_check_count {url_check_count}\n\n"

    m += "# HELP visit_count_today The number of visits today\n"
    m += "# TYPE visit_count_today gauge\n"
    m += f"visit_count_today {visit_count_today}\n\n"

    m += "# HELP check_url_duration The duration of URL checks in seconds\n"
    m += "# TYPE check_url_duration histogram\n"
    for bucket in histogram_buckets:
        m += f"check_url_duration{{le=\"{bucket}\"}} {histogram_data[bucket]}\n"
    m += f"check_url_duration_seconds{{le=\"+Inf\"}} {histogram_data['+Inf']}\n\n"

    m += "# HELP check_url_duration_summary The summary of URL check durations in seconds\n"
    m += "# TYPE check_url_duration_summary summary\n"
    m += f"check_url_duration_summary{{quantile=\"0.5\"}} {quantiles[0]}\n"
    m += f"check_url_duration_summary{{quantile=\"0.9\"}} {quantiles[1]}\n"
    m += f"check_url_duration_summary{{quantile=\"0.99\"}} {quantiles[2]}\n"
    m += f"check_url_duration_summary_count {len(response_times)}\n"
    m += f"check_url_duration_summary_sum {sum(response_times)}\n"
    
    return Response(m, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8080)
