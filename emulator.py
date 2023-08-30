import telnetlib
import time
import random

def connect_to_emulator(host, port, auth_token):
    try:
        emulator = telnetlib.Telnet(host, port)
        print("Connected to the emulator.")

        emulator.read_until(b"OK", timeout=10)
        emulator.write(f'auth {auth_token}\n'.encode())
        emulator.read_until(b"OK", timeout=10)
        print("Authenticated with the emulator.")

        return emulator
    except Exception as e:
        print("An error occurred:", e)
        return None

def set_sensor_data(emulator, sensor, x, y, z):
    try:
        command = f'sensor set {sensor} {x:.2f}:{y:.2f}:{z:.2f}\n'
        emulator.write(command.encode())
        emulator.read_until(b"OK", timeout=10)
        print(f"{sensor.capitalize()} data set:", command.strip())
    except Exception as e:
        print(f"An error occurred while setting {sensor} data:", e)

def generate_random_sensor_data():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-9.0, 9.0)
    z = random.uniform(1.5, -10.5)  # Simulate gravity effect
    return x, y, z

if __name__ == "__main__":
    emulator_host = "localhost"  # Replace with your emulator's IP address or hostname
    emulator_port = 5554  # Replace with your emulator's telnet port
    auth_token = "<>"  # Replace with your emulator's auth token

    emulator = connect_to_emulator(emulator_host, emulator_port, auth_token)
    if emulator:
        try:
            while True:
                accelerometer_data = generate_random_sensor_data()
                gyroscope_data = generate_random_sensor_data()

                set_sensor_data(emulator, "acceleration", *accelerometer_data)
                set_sensor_data(emulator, "gyroscope", *gyroscope_data)
                time.sleep(0.1)  # Set the time interval for sending data
        except KeyboardInterrupt:
            pass
        finally:
            emulator.close()
            print("Telnet connection closed.")
