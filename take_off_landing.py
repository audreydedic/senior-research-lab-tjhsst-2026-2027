from djitellopy import tello
import time

# instantiate drone object and connect to the drone
drone = tello.Tello()
drone.connect()

print("------------------------------------------")
print(f"battery level: {drone.get_battery()}%")
print("------------------------------------------")

print("------------------------------------------")
print(f"battery level: {drone.get_battery()}%")
print(f"temperature: {drone.get_highest_temperature()}°C")
print("------------------------------------------")

time.sleep(1)

# movement commands
drone.takeoff()
drone.move("forward",20)
drone.land()

# reboot/end tello drone object
drone.end()

