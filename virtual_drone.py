import pybullet as p
import time
import pybullet_data
import numpy as np

# connects to the physics simulator (GUI launches the graphical window, but DIRECT doesn't)
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally

# environment set up
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")

# objects
startPos = [0,0,0]
startOrientation = p.getQuaternionFromEuler([0,0,3])
droneId = p.loadURDF("/assets/racer.urdf",startPos, startOrientation)
startPos = [0,10,0]
startOrientation = p.getQuaternionFromEuler([1,0,2])
duckId = p.loadURDF("duck_vhacd.urdf",startPos, startOrientation)

def takeoff(droneId):
    for i in range(100):
        dronePos, droneOrn = p.getBasePositionAndOrientation(droneId)
        force = 20 * ([0,0,2] - np.array(dronePos))
        p.applyExternalForce(droneId, -1,force, dronePos, p.WORLD_FRAME)
        p.stepSimulation()
        time.sleep(1./240.)

takeoff(droneId)

# simulation loop
for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)

    dronePos, droneOrn = p.getBasePositionAndOrientation(droneId)
    duckPos, duckOrn = p.getBasePositionAndOrientation(duckId)

    force = 5 * ([duckPos[0],duckPos[1],1] - np.array(dronePos))
    p.applyExternalForce(droneId, -1,force, dronePos, p.WORLD_FRAME)

    # printing position for visuals
    if i % 10 == 0:
        x,y,z = dronePos
        x=round(x,2)
        y=round(y,2)
        z=round(z,2)
        dronePos=(x,y,z)
        x,y,z = duckPos
        x=round(x,2)
        y=round(y,2)
        z=round(z,2)
        duckPos=(x,y,z)

        x,y,z,w = droneOrn
        x=round(x,2)
        y=round(y,2)
        z=round(z,2)
        w=round(w,2)
        droneOrn=(x,y,z,w)
        x,y,z,w = duckOrn
        x=round(x,2)
        y=round(y,2)
        z=round(z,2)
        w=round(w,2)
        duckOrn=(x,y,z,w)

        print()
        print(f"Drone position:{dronePos}")
        # print(f"Orientation:{droneOrn}")
        print(f"Duck position:{duckPos}")
        # print(f"Orientation:{duckOrn}")


p.disconnect()