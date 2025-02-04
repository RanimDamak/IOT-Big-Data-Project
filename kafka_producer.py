import kafka_utils
import struct
import time
import random

def main():
    # Create a producer
    producer = kafka_utils.create_producer()

    while True:
        # Generate random vehicle data
        speed = random.gauss(80, 10)  # speed in km/h
        fuelflow = random.gauss(20, 5)  # fuel flow in liters/hour
        rpm = random.gauss(2400, 500)  # RPM

        randNumber = random.uniform(0,10)
        if (randNumber<=0.5):
          speed = 0
        elif (randNumber >=4):
          speed = random.uniform(60,70)
      
        # Ensure that the generated values are within the valid range
        speed = min(max(speed, 0), 120)
        fuelflow = min(max(fuelflow, 0), 40)
        rpm = min(max(rpm, 0), 4000)

        # Convert the float values to byte strings
        speed_bytes = struct.pack("!f", speed)
        fuelflow_bytes = struct.pack("!f", fuelflow)
        rpm_bytes = struct.pack("!f", rpm)

        # Combine the byte strings into a single message
        message = speed_bytes + fuelflow_bytes + rpm_bytes

        # Publish the data to the Kafka topic
        kafka_utils.publish_data(producer, message)

        speed = struct.unpack("!f", speed_bytes)[0]
        fuelflow = struct.unpack("!f", fuelflow_bytes)[0]
        rpm = struct.unpack("!f", rpm_bytes)[0]
        print("Speed:", speed)
        print("Fuel flow:", fuelflow)
        print("RPM: ", rpm)

        # Wait 1 second
        time.sleep(1)

if __name__ == "__main__":
  main()