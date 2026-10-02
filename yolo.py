import cv2
from ultralytics import YOLO, solutions
import numpy as np

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

def main():
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, detected_objects, depth = detect_objects_depth(frame)

        print("-----------------------")
        print(depth)
        print("-----------------------")

        cv2.imshow("YOLO Vision", frame)
        if detected_objects:
            print("Detected objects:", detected_objects)
        key = cv2.waitKey(1) & 0xFF

        if('person' in detected_objects and depth > 20):
            print("MOVING FORWARD")
        else:
            print("STOPPED")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()