from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://127.0.0.1:5501")

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

if __name__ == '__main__':
    app.run(debug=True)
