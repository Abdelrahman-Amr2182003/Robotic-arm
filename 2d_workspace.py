import numpy as np
import matplotlib.pyplot as plt
import roboticstoolbox as rtb
from spatialmath import SE3

# Define the robot using previously defined properties
robot_properties = [
    {'d': 78.3, 'a': 0, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 86.83, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 100.47, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'d': 0, 'a': 70.13 + 134.49, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 0, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])}
]
robot = rtb.DHRobot([rtb.RevoluteDH(**params) for params in robot_properties], name='CustomRobot')

# Maximum theoretical reach
max_reach = sum(p['a'] for p in robot_properties)

# Grid resolution and range
resolution = 100
x = np.linspace(-max_reach, max_reach, resolution)
y = np.linspace(-max_reach, max_reach, resolution)
X, Y = np.meshgrid(x, y)

# Initialize the reachability matrix
reachability = np.zeros(X.shape, dtype=bool)

# Check reachability of each point in the XY-plane
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        point = np.array([X[i, j], Y[i, j], 0])  # We consider only XY plane (Z=0)
        if np.linalg.norm(point) <= max_reach:  # Check if within maximum reach
            try:
                T = SE3(point) * SE3.Rz(0)  # Target pose
                sol = robot.ikine_LM(T)  # Solve inverse kinematics
                if sol.success:  # If IK solution found
                    reachability[i, j] = True
            except:
                continue

# Plotting
plt.figure(figsize=(10, 10))
plt.pcolormesh(X, Y, reachability, shading='auto', color='green', alpha=0.5)
plt.colorbar(label='Reachable')
plt.title('2D Reachability Map for Robot')
plt.xlabel('X [mm]')
plt.ylabel('Y [mm]')
plt.axis('equal')
plt.grid(True)

# Save the figure
plt.savefig('2D_Reachability_Map.png')
plt.show()
