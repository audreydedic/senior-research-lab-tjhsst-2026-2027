import math
from djitellopy import tello
import time
import numpy as np
import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

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

                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame, detected_objects

def process_tello_video(drone):
    while True:
        frame=drone.get_frame_read().frame # get the frames from tello
        frame,detected_objects = detect_objects(frame)

        # print(detected_objects) # list of detected labels
        if('person' in detected_objects):
            drone.move_forward(200)

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