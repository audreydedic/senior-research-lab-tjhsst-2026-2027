from djitellopy import tello
import time

# instantiate drone object and connect to the drone
drone = tello.Tello()
drone.connect()

print("*****************************************")
print(f"battery level: {drone.get_battery()}%")
print("*****************************************")

time.sleep(1)

# movement commands
drone.takeoff()
drone.rotate_clockwise(360)
drone.land()

# reboot/end tello drone object
drone.end()

