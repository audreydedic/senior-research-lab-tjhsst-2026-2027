import math
from djitellopy import tello
import time
import numpy as np
import cv2

def moveToPosition(drone,v):
    # v is an point vector from [0,0,0] to any desired point
    x,y = v[0],v[1]
    distance = math.sqrt(x**2 + y**2)

    angle = math.atan(y/x)
    if(angle==-0.0):
        angle=2*math.pi
    angle = angle*(180/math.pi)

    drone.rotate_clockwise(int(angle)*2*-1)
    drone.move_forward(int(distance + 20))

    # return distance, angle

def process_tello_video(drone):
    while True:
        frame=drone.get_frame_read().frame # get the frames from tello
        cv2.imshow("Frame",frame) # display frames obtained from tello
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break # breaks out of while loop from q key
    cv2.destroyAllWindows()
    drone.end()

def main():
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

    # camera streaming for drone
    drone.streamon()

    time.sleep(1)
    # drone.takeoff()

    # moves drone in square (works)
    # moveToPosition(drone,[50,50])
    # moveToPosition(drone,[50,50])
    # moveToPosition(drone,[50,50])
    # moveToPosition(drone,[50,50])
    process_tello_video(drone)


    # cosine movement back and forth from simulation
    # PERIOD = 20
    # NUM_WP =  48*PERIOD
    # TARGET_POS = np.zeros((NUM_WP, 2))
    # for i in range(NUM_WP):
    #     TARGET_POS[i, :] = [0.5*np.cos(2*np.pi*(i/NUM_WP)), 0]

    # for i in range(len(TARGET_POS)):
    #     x,y = TARGET_POS[i][0]*100,TARGET_POS[i][1]*100
    #     print(x,y)
    #     angle = math.atan(y/x)
    #     if(angle==-0.0):
    #         angle=math.pi
    #     angle = angle*(180/math.pi)
    #     print(angle)

        # if(i%10 ==0):
        #     time.sleep(.5)
        #     moveToPosition(drone,[TARGET_POS[i][0]*100,TARGET_POS[i][1]*100])

if __name__ == "__main__":
    main()