from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
vehicle_data_collection = client.vehicle_data.kpi

@app.route('/')
def dashboard():
  # Render the dashboard template
  return render_template('dashboard.html')

@app.route('/kpi', methods=['GET'])
def get_vehicle_data():
  # Query the database for the latest vehicle data
  vehicle_data = vehicle_data_collection.find().sort('_id', -1).limit(1)[0]

  # Convert the ObjectId values to strings
  vehicle_data["_id"] = str(vehicle_data["_id"])

  # Return the data as a JSON response
  return jsonify(vehicle_data)

if __name__ == '__main__':
  app.run()
