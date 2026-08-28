import pybullet as p
import time
import pybullet_data

# connects to the physics simulator (GUI launches the graphical window, but DIRECT doesn't)
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version

# import pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally

# gravity is represented as a 3D vector (in this case, -10 like -9.8m/s^2)
p.setGravity(0,0,-10)

# loads a pre made physics model from a "Universal Robot Description File" (URDF)
planeId = p.loadURDF("plane.urdf")

# starting position and orientation
startPos = [0,0,1]
startOrientation = p.getQuaternionFromEuler([0,0,0])

boxId = p.loadURDF("r2d2.urdf",startPos, startOrientation)
#set the center of mass frame (loadURDF sets base link frame) startPos/Ornp.resetBasePositionAndOrientation(boxId, startPos, startOrientation)
for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
p.disconnect()

# this script DOES NOT BELONG TO ME and was rather taken from this pybullet documentation: 
# https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit?tab=t.0
# Script from the on "Hello PyBullet" section

# I have added additional markups on it for learning purposes only