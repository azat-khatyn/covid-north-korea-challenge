from flask import Flask
from flask import request
from datetime import date, timedelta
import pandas as pd

app = Flask(__name__)

@app.route('/confirmed_cases_estimation', methods=['GET'])
def confirmed_cases_estimation():
    try:
        days = int(request.args.get('days'))
        if days < 0:
            return 'No covid data is available prior to the 1st of March 2020!'
        date_of_prediction = (date(2020, 3, 1) + timedelta(days=days)).isoformat().replace('-0', '-', 2)

        covid_data = pd.read_csv('covid_data.csv')
        covid_data_on_date_of_prediction = covid_data[covid_data['date'] == date_of_prediction].drop(['date'], axis=1)

        if covid_data_on_date_of_prediction.shape[0] == 0:
            return 'No covid data is available yet for the date %s' % date_of_prediction

        k_nearest_neighbors_to_nk = pd.read_csv('nearest_countries_to_nk.csv')

        countries_mapping = {
            'Myanmar': 'Burma',
            'Virgin Islands (U.S.)': '',
            'Mali': 'Mali',
            'Kazakhstan': 'Kazakhstan',
            'Papua New Guinea': 'Papua New Guinea',
            'Cambodia': 'Cambodia'
        }

        k_nearest_neighbors_to_nk_mapped_names = \
            pd.DataFrame(k_nearest_neighbors_to_nk.apply(lambda row: countries_mapping[row['name']], axis=1), columns=['country'])
        k_nearest_neighbors_to_nk_mapped_names = k_nearest_neighbors_to_nk_mapped_names[k_nearest_neighbors_to_nk_mapped_names['country'] != '']

        nearest_countries_on_date_of_prediction = pd.merge(k_nearest_neighbors_to_nk_mapped_names, covid_data_on_date_of_prediction, on='country')

        confirmed = int(round(nearest_countries_on_date_of_prediction['confirmed'].mean()))
        return 'On the date %s the estimated number of confirmed cases in North Korea is %d' % (date_of_prediction, confirmed)
    except Exception as exc:
        return 'Internal error: %s' % exc
