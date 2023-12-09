from flask import Flask, jsonify, request, render_template
import pandas as pd
from sqlalchemy import create_engine
from flask_cors import CORS

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5501"], methods=["GET", "POST"])

# Replace these values with your MySQL server details
host = "localhost"
user = "root"
password = "Shama0207"
database = "project"

# Create an SQLAlchemy engine using the MySQL connector connection
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Specify the name of your MySQL table
table_name = 'your_table_name'


def get_data(query):
    region_data = pd.read_sql_query(query, con=engine)
    data = {
        'labels': list(region_data['REGION']),
        'values': list(region_data['total_MML']),
        'type': 'pie',
        'hole': 0.3
    }
    return data


def get_state_data(query):
    state_data = pd.read_sql_query(query, con=engine)
    data = {
        'labels': list(state_data['STATE_UT']),
        'values': list(state_data['total_MML']),
        'type': 'pie',
        'hole': 0.3
    }
    return data


def fetch_district_data(state, severity):
    if severity == 'MILD':
        query_men = f"SELECT DISTRICT_NAME, MMl AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
        query_women = f"SELECT DISTRICT_NAME, WMl AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
    elif severity == 'MODERATE':
        query_men = f"SELECT DISTRICT_NAME, MMo AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
        query_women = f"SELECT DISTRICT_NAME, WMo AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
    elif severity == 'EXTREME':
        query_men = f"SELECT DISTRICT_NAME, MExt AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
        query_women = f"SELECT DISTRICT_NAME, WExt AS total_MML FROM {table_name} WHERE STATE_UT = '{state}'"
    else:
        return jsonify({'error': 'Invalid severity selected'})

    men_data = pd.read_sql_query(query_men, con=engine)
    women_data = pd.read_sql_query(query_women, con=engine)

    men_values = list(men_data['total_MML'])
    women_values = list(women_data['total_MML'])

    return {
        'districts': list(men_data['DISTRICT_NAME']),
        'menValues': men_values,
        'womenValues': women_values
    }


# Home route to render HTML template
@app.route('/')
def home():
    return render_template('index.html')


# Region-wise data
@app.route('/get_data_MMl')
def get_data_MMl():
    query_MMl = f"SELECT REGION, SUM(MML) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_MMl))


@app.route('/get_data_MMo')
def get_data_MMo():
    query_MMo = f"SELECT REGION, SUM(MMo) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_MMo))


@app.route('/get_data_MExt')
def get_data_MExt():
    query_MExt = f"SELECT REGION, SUM(MExt) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_MExt))


@app.route('/get_data_WMl')
def get_data_WMl():
    query_WMl = f"SELECT REGION, SUM(WML) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_WMl))


@app.route('/get_data_WMo')
def get_data_WMo():
    query_WMo = f"SELECT REGION, SUM(WMo) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_WMo))


@app.route('/get_data_WExt')
def get_data_WExt():
    query_WExt = f"SELECT REGION, SUM(WExt) AS total_MML FROM {table_name} GROUP BY REGION"
    return jsonify(get_data(query_WExt))


# State-wise data
@app.route('/get_state_data_MMl')
def get_state_data_MMl():
    query_MMl = f"SELECT STATE_UT, SUM(MML) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_MMl))


@app.route('/get_state_data_MMo')
def get_state_data_MMo():
    query_MMo = f"SELECT STATE_UT, SUM(MMo) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_MMo))


@app.route('/get_state_data_MExt')
def get_state_data_MExt():
    query_MExt = f"SELECT STATE_UT, SUM(MExt) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_MExt))


@app.route('/get_state_data_WMl')
def get_state_data_WMl():
    query_WMl = f"SELECT STATE_UT, SUM(WML) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_WMl))


@app.route('/get_state_data_WMo')
def get_state_data_WMo():
    query_WMo = f"SELECT STATE_UT, SUM(WMo) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_WMo))


@app.route('/get_state_data_WExt')
def get_state_data_WExt():
    query_WExt = f"SELECT STATE_UT, SUM(WExt) AS total_MML FROM {table_name} GROUP BY STATE_UT"
    return jsonify(get_state_data(query_WExt))


# Handle district data request
@app.route('/get_district_data', methods=['POST'])
def handle_district_data():
    data = request.get_json()
    state = data.get('state')
    severity = data.get('severity')

    try:
        district_data = fetch_district_data(state, severity)
        return jsonify(district_data)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
