import math
import struct
import time
from pymongo import MongoClient
from kafka import KafkaConsumer

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_data"]

# Initialize variables for tracking KPI values
prev_speed = 0  # for sudden acceleration/deceleration
max_speed = 0  # for maximum speed
min_speed = float("inf")  # for minimum speed
sum_speed = 0  # for velocity standard deviation
sum_speed_squared = 0  # for velocity standard deviation
num_data_points = 0
idling_start_time = None  # for idling
cruising_start_time = None  # for cruising
cruising_speed_values = []  # for cruising
fuel_consumptions = []  # for fuel consumption

def store_data(kpi_values):
  # Insert the KPI values into the "kpi" collection
  db.kpi.insert_one(kpi_values)

def update_dashboard(speed, fuelflow, rpm):
  # Calculate the KPIs based on the vehicle data
  global prev_speed, max_speed, min_speed, sum_speed, sum_speed_squared, idling_start_time, cruising_start_time, cruising_speed_values
  global num_data_points

  # Initialize an empty object to store the KPI values
  kpi_values = {}
  kpi_values["speed"] = speed
  kpi_values["rpm"] = rpm
  # Calculate sudden acceleration/deceleration
  threshold = 9.87926
  if abs(speed - prev_speed) > threshold:
    if speed > prev_speed:
      kpi_values["sudden_acceleration"] = True
      kpi_values["sudden_deceleration"] = False
    else:
      kpi_values["sudden_deceleration"] = True
      kpi_values["sudden_acceleration"] = False
  else:
    kpi_values["sudden_deceleration"] = False
    kpi_values["sudden_acceleration"] = False
  prev_speed = speed

  # Update maximum and minimum speed
  max_speed = max(max_speed, speed)
  kpi_values["max_speed"] = max_speed

  # Update sum and sum of squares of speed values for velocity standard deviation
  sum_speed += speed
  sum_speed_squared += speed ** 2
  num_values = len(fuel_consumptions) + 1
  mean_speed = sum_speed / num_values
  std_speed = math.sqrt((sum_speed_squared / num_values) - (mean_speed ** 2))
  kpi_values["average_speed"] = mean_speed
  kpi_values["velocity_std_dev"] = std_speed

  # Check for high RPM
  threshold_rpm = 3000  # for gasoline
  if rpm > threshold_rpm and speed != 0:
    kpi_values["high_rpm"] = True
  else:
    kpi_values["high_rpm"] = False

  # Check for idling
  if rpm > 0 and speed == 0:
    kpi_values["idling"] = True
  else:
    kpi_values["idling"] = False

  # Check for cruising
  if cruising_start_time is not None:
    cruising_speed_values.append(speed)
    if len(cruising_speed_values) >= 3:  # check cruising conditions over the last 5 seconds
      mean_speed = sum(cruising_speed_values) / len(cruising_speed_values)
      std_speed = math.sqrt((sum(x ** 2 for x in cruising_speed_values) / len(cruising_speed_values)) - (mean_speed ** 2))
      if mean_speed > 60 and std_speed < 1.5:
        kpi_values["cruising"] = True
      else:
        # Reset cruising variables
        kpi_values["cruising"] = False
        cruising_start_time = None
        cruising_speed_values = []
  elif speed > 60:
    cruising_start_time = time.time()
    cruising_speed_values = [speed]
  else:
    kpi_values["cruising"] = False

  # Calculate fuel consumption
  if speed > 0:
    fuel_consumption = fuelflow / speed
    fuel_consumptions.append(fuel_consumption)
    kpi_values["fuel_consumption"] = fuel_consumption
  else:
    kpi_values["fuel_consumption"] = 0
  return kpi_values

class KpiProcessor:
  def process(self, speed, fuelflow, rpm):
    kpi_values = update_dashboard(speed, fuelflow, rpm)
    store_data(kpi_values)

class KpiConsumer:
  def __init__(self, consumer: KafkaConsumer, processor: KpiProcessor):
    self.consumer = consumer
    self.processor = processor

  def poll(self):
    for message in self.consumer:
      value = message.value
      speed, fuelflow, rpm = struct.unpack("!fff", value)
      self.processor.process(speed, fuelflow, rpm)

def main():
  # Create a Kafka consumer and a Kafka producer
  consumer = KafkaConsumer(
      "vehicle-data",
      bootstrap_servers=["localhost:9092"],
      value_deserializer=lambda value: value,  # return the raw byte string
  )

  # Create a KpiProcessor and a KpiConsumer
  processor = KpiProcessor()
  kpi_consumer = KpiConsumer(consumer, processor)

  # Start the stream processing loop
  while True:
    kpi_consumer.poll()

if __name__ == "__main__":
  main()
