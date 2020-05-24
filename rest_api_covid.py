from flask import Flask
from flask import request
from datetime import date, timedelta

app = Flask(__name__)

@app.route('/confirmed_cases_estimation', methods=['GET'])
def confirmed_cases_estimation():
    try:
        days = int(request.args.get('days'))
        date_of_prediction = date(2020, 3, 1) + timedelta(days=days)
        return date_of_prediction.isoformat()
    except Exception as exc:
        return 'Internal error: %s' % exc
