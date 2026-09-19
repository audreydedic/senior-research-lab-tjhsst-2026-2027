import math
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

drone.takeoff()

def moveToPosition(drone,v):
    # v is an point vector from [0,0,0] to any desired point
    x,y = v[0],v[1]
    distance = math.sqrt(x**2 + y**2)

    angle = math.atan(y/x)
    angle = angle*(180/math.pi)

    drone.rotate_counter_clockwise(int(angle)*2)
    drone.move_forward(int(distance))

    # return distance, angle

# print(moveToPosition([1,2,3]))

moveToPosition(drone,[100,100])
moveToPosition(drone,[100,100])
moveToPosition(drone,[100,100])
moveToPosition(drone,[100,100])