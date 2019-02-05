from datadog import initialize, api
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import time

options = {
    'api_key': 'fa9c0930cb9927c77b480f0c9a8c08bc',
    'app_key': 'cd26bb41159733eafbd4e7af58cf00c89d715348'
}

initialize(**options)

def docker_cpu_usage():
  now = int(time.time())
  query = 'docker.cpu.usage{*}by{host}'
  queryResults = api.Metric.query(start=now - 3600, end=now, query=query)
  qR = queryResults['series']
  point_list = qR[0]['pointlist']
  return point_list

app = Flask(__name__)
CORS(app)

@app.route('/api/delete_dashboard', methods=['POST'])
def delete_dashboard():
  wasSuccess = False
  if 'id' in request.form:
    id = request.form['id']
    api.DashboardList.delete(int(id))
    wasSuccess = True
  return jsonify({'Success': wasSuccess})

@app.route('/api/create_dashboard', methods=['POST'])
def create_dashboard():
  wasSuccess = False
  if 'name' in request.form:
    name = request.form['name']
    api.DashboardList.create(name=name)
    wasSuccess = True
  return jsonify({'Success': wasSuccess})

@app.route("/api/get_dashboards")
def get_all_dashboards():
  return jsonify(api.DashboardList.get_all())

@app.route("/api/cpu_usage")
def get_cpu():
  return jsonify(docker_cpu_usage())

if __name__ == "__main__":
  app.run(debug=True)


