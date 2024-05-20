import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3
import matplotlib.pyplot as plt

# Define the robot
robot_properties = [
    {'d': 78.3, 'a': 0, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 86.83, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 100.47, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'d': 0, 'a': 70.13 + 134.49, 'alpha': np.pi / 2, 'offset': 0, 'qlim': np.radians([-180, 180])},
    {'a': 0, 'd': 0, 'alpha': 0, 'offset': 0, 'qlim': np.radians([-180, 180])}
]
robot = rtb.DHRobot([rtb.RevoluteDH(**params) for params in robot_properties], name='CustomRobot')

# Sampling configurations
num_samples = 1000
points = np.zeros((num_samples, 3))
for i in range(num_samples):
    # Randomly sample joint angles within their limits
    q = np.random.uniform(low=[p['qlim'][0] for p in robot_properties],
                          high=[p['qlim'][1] for p in robot_properties])
    # Calculate the forward kinematics
    T = robot.fkine(q)
    # Extract the position of the end-effector
    points[i, :] = T.t

# Plot reachable workspace
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, alpha=0.1)
ax.set_title('Reachable Workspace of Custom Robot')
ax.set_xlabel('X [mm]')
ax.set_ylabel('Y [mm]')
ax.set_zlabel('Z [mm]')
plt.show()

# Save the figure
fig.savefig('Reachable_Workspace.png')

# Calculate and print the bounds
x_min, x_max = points[:, 0].min(), points[:, 0].max()
y_min, y_max = points[:, 1].min(), points[:, 1].max()
z_min, z_max = points[:, 2].min(), points[:, 2].max()

print(f"x_min: {x_min}, x_max: {x_max}")
print(f"y_min: {y_min}, y_max: {y_max}")
print(f"z_min: {z_min}, z_max: {z_max}")
