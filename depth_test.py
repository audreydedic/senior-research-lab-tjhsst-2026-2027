from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO("yolo26n-depth.pt")
results = model.predict("horse.jpg",save=True,device="mps")
results = results[0]

depth_numpy = results.depth.data.cpu().numpy()

x,y=300,300
distance = depth_numpy[y,x]

np.save("depth.npy",depth_numpy)
depth_numpy_loaded = np.load("depth.npy")

# visualization with colorization
from ultralytics.utils.plotting import colorize_depth

metric_visualization = colorize_depth(
    depth_numpy,cmap="spectral",mode="disparity",
)

cv2.imwrite("disparity.png",metric_visualization)

# calibration step