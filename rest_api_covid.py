from flask import Flask
from flask import request
from datetime import date, timedelta
import pandas as pd
import json

app = Flask(__name__)

@app.route('/confirmed_cases_estimation', methods=['GET'])
def confirmed_cases_estimation():
    try:
        days = int(request.args.get('days'))
        if days < 0:
            return 'No covid data is available prior to the 1st of March 2020!'

        date_of_prediction = (date(2020, 3, 1) + timedelta(days=days)).isoformat().replace('-0', '-', 2)

        # reading covid data and filtering by the input date
        covid_data = pd.read_csv('covid_data.csv')
        covid_data_on_date_of_prediction = covid_data[covid_data['date'] == date_of_prediction].drop(['date'], axis=1)

        if covid_data_on_date_of_prediction.shape[0] == 0:
            return 'No covid data is available yet for the date %s' % date_of_prediction

        # reading country names mappings
        fh = open('countries_mapping.json', 'r')
        countries_mapping = json.load(fh)
        fh.close()

        def map_country_name(row):
            if row['name'] in countries_mapping:
                return countries_mapping[row['name']]
            else:
                return ''

        # reading nearest countries data and mapping country names
        k_nearest_countries = pd.read_csv('nearest_countries.csv')
        k_nearest_countries_mapped_names = \
            pd.DataFrame(k_nearest_countries.apply(lambda row: map_country_name(row), axis=1), columns=['country'])

        # joining nearest countries DF and covid data DF
        nearest_countries_on_date_of_prediction = pd.merge(k_nearest_countries_mapped_names, covid_data_on_date_of_prediction, on='country')

        # taking average number of confirmed cases among nearest countries
        confirmed = int(round(nearest_countries_on_date_of_prediction['confirmed'].mean()))
        return 'On the date %s the estimated number of confirmed cases in North Korea is %d' % (date_of_prediction, confirmed)
    except Exception as exc:
        return 'Internal error: %s' % exc
