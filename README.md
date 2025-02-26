
# Vehicle Data Processing and Dashboard

This project processes vehicle data in real-time using Kafka and MongoDB and displays the data on a dashboard. It calculates Key Performance Indicators (KPIs) such as sudden acceleration, high RPM, cruising, idling, and fuel consumption.

## Table of Contents
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [KPIs Calculated](#kpis-calculated)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used
- Python
- Kafka
- MongoDB
- Flask (for the dashboard)
- HTML, CSS, and JavaScript (for front-end)

## Project Structure
```
.
├── __pycache__/
├── templates/
│   ├── dashboard.html
│   └── main.js
├── LICENSE
├── kafka_consumer.py
├── kafka_producer.py
├── kafka_utils.py
└── main.py
```

- `kafka_producer.py`: Generates and sends simulated vehicle data to Kafka.
- `kafka_consumer.py`: Consumes vehicle data from Kafka, calculates KPIs, and stores them in MongoDB.
- `kafka_utils.py`: Utility functions for Kafka producer and consumer.
- `templates/dashboard.html`: Displays vehicle data and KPIs on a dashboard.
- `main.py`: Starts the Flask web server for the dashboard.

## Setup and Installation
1. **Install Required Packages:**
   Make sure you have Python and the following packages installed:
   ```sh
   pip install kafka-python pymongo Flask
   ```
   
2. **Start MongoDB:**
   Ensure MongoDB is running on `localhost:27017`.

3. **Start Kafka:**
   Make sure Kafka is running on `localhost:9092`. You can download Kafka from [Apache Kafka](https://kafka.apache.org/downloads).

4. **Create Kafka Topic:**
   Create a Kafka topic named `vehicle-data` using the following command:
   ```sh
   bin/kafka-topics.sh --create --topic vehicle-data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

## Usage
1. **Start the Kafka Producer:**
   ```sh
   python kafka_producer.py
   ```

2. **Start the Kafka Consumer:**
   ```sh
   python kafka_consumer.py
   ```

3. **Start the Dashboard:**
   ```sh
   python main.py
   ```
   Visit `http://localhost:5000` to view the dashboard.

## KPIs Calculated
- **Sudden Acceleration/Deceleration:** Detects sudden changes in speed.
- **Maximum Speed:** Tracks the maximum speed recorded.
- **Velocity Standard Deviation:** Measures the variability in speed.
- **High RPM:** Detects high RPM values that may indicate aggressive driving.
- **Idling:** Checks if the vehicle is idling (non-zero RPM but zero speed).
- **Cruising:** Detects cruising state based on speed consistency.
- **Fuel Consumption:** Calculates fuel consumption efficiency.

## Dashboard
The dashboard is implemented using Flask and displays:
- Real-time vehicle data: Speed, Fuel Flow, RPM.
- KPIs: Sudden Acceleration, High RPM, Idling, Cruising, Fuel Consumption.
```
