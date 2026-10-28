import cv2
from ultralytics import YOLO, solutions
import numpy as np
import math

# Load models2
model = YOLO("yolonano.pt")
model2 = YOLO("yolov8n.pt")
depth_model = YOLO("yolo26n-depth.pt")

def detect_objects_depth(frame):
    frame = cv2.resize(frame,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
    detected_objects = []
    coordinates = []
    DETECT_THIS_LABEL = 'head'
    person_detected=False
    
    # bounding boxes (object detection)
    results = model2(frame)
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get class ID
            confidence = box.conf[0].item()  # Confidence score

            if confidence > 0.5:
                label = model2.names[class_id]
                if label=='person':
                    person_detected=True

    # bounding boxes (object detection)
    results = model(frame)
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])  # Get class ID
            confidence = box.conf[0].item()  # Confidence score

            if confidence > 0.5:
                    label = model.names[class_id]
                # if label==DETECT_THIS_LABEL:
                    detected_objects.append(label)
                    # Draw bounding box removed since distance calc draws boxes for camera
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    coordinates.append([x1, y1, x2, y2])
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # depth perception
    depth_of_object = math.inf
    results = depth_model(frame)
    for r in results:
        depth_heatmap = r.plot()
        depth_map = r.depth.data.cpu().numpy()

        coors = [0,1,0,1]
        for i in range(len(detected_objects)):
            if detected_objects[i]==DETECT_THIS_LABEL:
                coors = coordinates[i]
        x1=coors[0]
        y1=coors[1]
        x2=coors[2]
        y2=coors[3]
        # x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        region_depth = depth_map[y1:y2,x1:x2]
        # if(np.median(region_depth)<depth_of_object):
        depth_of_object = np.median(region_depth)
            # x1=coors[0]
            # y1=coors[1]
            # x2=coors[2]
            # y2=coors[3]

    frame = depth_heatmap

    centerX,centerY = ((coors[0]+coors[2])/2), ((coors[1]+coors[3])/2)
    center_coors = (centerX,centerY)

    if(depth_of_object== math.inf or np.isnan(depth_of_object)): #np.isnan(depth_of_object)):
        depth_of_object=0
    
    depth = int(depth_of_object*100)
    height,width,channels = frame.shape
    horizontal_displacement=centerX-(width/2)
    vertical_displacement=(centerY-(height/2))*-1

    # draw boxes around detected objs
    for i in range(len(detected_objects)):
        c = coordinates[i]
        l = detected_objects[i]
        x1=c[0]
        y1=c[1]
        x2=c[2]
        y2=c[3]
        if(x1==coors[0] and y1==coors[1] and x2 == coors[2] and y2==coors[3]):
            label = f"{l}: {depth}cm"
        else: label = l
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    print()
    print("-----------------------------------------------------------")
    print(f"Depth of nearest person: {depth}cm")
    # print(f"Min/max coordinates of object: ({coors[0]},{coors[1]}) , ({coors[2]},{coors[3]})")
    # print(f"Center coordinate of object: {center_coors}")
    print(f"Displacement: {horizontal_displacement}")
    print("-----------------------------------------------------------")

    x = int(centerX)
    y = int(centerY)

    # draw center points
    cv2.circle(frame,(x,y), 10, (255,255,255), -1)
    cv2.circle(frame,(int(width/2),int(height/2)), 10, (0,255,0), -1)

    cv2.putText(frame, f"horizontal displacement: {horizontal_displacement}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"vertical displacement: {vertical_displacement}", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame, detected_objects, depth, horizontal_displacement, vertical_displacement, person_detected

# def detect_objects(frame):
#     results = model(frame)
#     detected_objects = []

#     for r in results:
#         for box in r.boxes:
#             class_id = int(box.cls[0])  # Get class ID
#             confidence = box.conf[0].item()  # Confidence score

#             if confidence > 0.5:
#                 label = model.names[class_id]
#                 detected_objects.append(label)

#                 # Draw bounding box removed since distance calc draws boxes for camera
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#     return frame, detected_objects

def main():
    cap = cv2.VideoCapture(0)  # Open webcam

    # toggle_frame = True
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # if frame_count%2==0:

        frame, detected_objects, depth, displacement, vertical_displacement,person_detected = detect_objects_depth(frame)

        print("VERTICAL DISPLACEMENT***************")
        print(vertical_displacement)
        print("*************************")

        print(f"Person detected: {person_detected}")

        cv2.imshow("YOLO Vision", frame)

        frame_count+=1
        key = cv2.waitKey(1) & 0xFF

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()