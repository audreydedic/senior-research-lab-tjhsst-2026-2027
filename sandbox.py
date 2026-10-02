import math
from djitellopy import tello
import time
import numpy as np
import cv2
from ultralytics import YOLO

# Load model
model = YOLO("yolo26n.pt")

# depth one
depth_model = YOLO("yolo26n-depth.pt")

def detect_objects_depth(frame):
    detected_objects = []
    coordinates = []
    
    # bounding boxes (object detection)
    results = model(frame)
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get class ID
            confidence = box.conf[0].item()  # Confidence score

            if confidence > 0.5:
                label = model.names[class_id]
                detected_objects.append(label)

                # Draw bounding box removed since distance calc draws boxes for camera
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                coordinates.append([x1, y1, x2, y2])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


    # depth perception
    depth_of_object = 0
    results = depth_model(frame)
    for r in results:
        depth_heatmap = r.plot()
        depth_map = r.depth.data.cpu().numpy()

        coors = [0,1,0,1]
        for i in range(len(detected_objects)):
            if detected_objects[i]=='person':
                coors = coordinates[i]
        x1=coors[0]
        y1=coors[1]
        x2=coors[2]
        y2=coors[3]
        # x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        region_depth = depth_map[y1:y2,x1:x2]
        depth_of_object = np.median(region_depth)

    frame = depth_heatmap

    print()
    print(depth_of_object)
    print()

    if(np.isnan(depth_of_object)):
        depth_of_object=0
    
    depth = int(depth_of_object*100)

    return frame, detected_objects, depth

def detect_objects(frame):
    results = model(frame)
    detected_objects = []

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get class ID
            confidence = box.conf[0].item()  # Confidence score

            if confidence > 0.5:
                label = model.names[class_id]
                detected_objects.append(label)

                # Draw bounding box removed since distance calc draws boxes for camera
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame, detected_objects

def process_tello_video(drone):
    STOPPING_DISTANCE=200
    SPEED=200

    while True:
        frame=drone.get_frame_read().frame # get the frames from tello
        frame,detected_objects,depth = detect_objects_depth(frame)

        print("-----------------------")
        print(depth)
        print("-----------------------")

        # print(detected_objects) # list of detected labels
        if('person' in detected_objects and depth > STOPPING_DISTANCE):
            drone.move_forward(SPEED)

        cv2.imshow("Drone Camera",frame) # display frames obtained from tello
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
    drone.takeoff()
    drone.move_up(50)

    process_tello_video(drone)

if __name__ == "__main__":
    main()