# TurtleBot3 Color Based Navigation using ROS2 and OpenCV

## Overview

This project implements autonomous color-based navigation for TurtleBot3 using ROS2 Humble, OpenCV, and Gazebo simulation.

The robot detects a green spherical object using computer vision techniques and autonomously aligns and moves toward the target using a proportional controller (P-controller).

The implementation includes:

- TurtleBot3 Gazebo simulation
- Real-time camera feed processing
- HSV color thresholding
- Contour detection
- Target center calculation
- P-controller based angular correction
- Autonomous object following
- Obstacle proximity detection using LiDAR

---

# Demo Video

## Watch the Project Demonstration

Click the link below to view the complete screen recording of the project execution:

[▶ Watch Demo Video on Google Drive](https://drive.google.com/file/d/1BpuBhFVfFWjwhDi-OHeJ47d2byQAdvx3/view?usp=drive_link)

---

# Problem Statement

Implement Color based Navigation with ROS2 and OpenCV:

1. Setup TurtleBot3 Gazebo simulation.
2. Subscribe to raw camera image topic.
3. Detect green object using OpenCV.
4. Compute contour center and image error.
5. Rotate robot using P-controller.
6. Move toward object when aligned.
7. Handle object loss and recovery.
8. Stop robot when close to obstacle.

---

# Technologies Used

- ROS2 Humble Hawksbill
- TurtleBot3
- Gazebo
- OpenCV
- Python3
- cv_bridge
- RQt Image View

---

# System Requirements

- Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic
- Python3
- OpenCV
- TurtleBot3 packages

---

# Installation

## Clone Repository

```bash
git clone https://github.com/priyanshum2142/ros2_color_navigation.git

cd ros2_color_navigation
```

---

# Install Dependencies

```bash
sudo apt update

sudo apt install ros-humble-turtlebot3* -y

sudo apt install python3-opencv -y

sudo apt install ros-humble-cv-bridge -y

sudo apt install ros-humble-gazebo-ros-pkgs -y
```

---

# Build Workspace

```bash
cd ~/ros2_color_navigation/ros2_ws_pri

colcon build
```

---

# Source Workspace

```bash
source /opt/ros/humble/setup.bash

source ~/ros2_color_navigation/ros2_ws_pri/install/setup.bash
```

---

# Launch Simulation

## Set TurtleBot3 Model

```bash
export TURTLEBOT3_MODEL=waffle_pi
```

---

## Launch Gazebo World

```bash
ros2 launch tb3_custom_world green_sphere_world.launch.py
```

This launches:
- TurtleBot3
- LiDAR
- Camera
- Green sphere target

---

# Run Color Navigation Node

Open a NEW terminal:

```bash
source /opt/ros/humble/setup.bash

source ~/ros2_color_navigation/ros2_ws_pri/install/setup.bash
```

Run:

```bash
ros2 run color_navigation color_follower
```

---

# Camera Feed Visualization

Open another terminal:

```bash
ros2 run rqt_image_view rqt_image_view
```

Select:

```bash
/camera/image_raw
```

---

# Useful ROS2 Commands

## List Topics

```bash
ros2 topic list
```

---

## Check Camera Frequency

```bash
ros2 topic hz /camera/image_raw
```

---

## Monitor Velocity Commands

```bash
ros2 topic echo /cmd_vel
```

---

## View Node Graph

```bash
ros2 run rqt_graph rqt_graph
```

---

# Working Principle

## 1. Image Subscription

The node subscribes to:

```bash
/camera/image_raw
```

using ROS2 image transport.

---

## 2. OpenCV Processing

The image is converted from ROS image format to OpenCV format using:

```python
cv_bridge
```

Then:
- BGR image → HSV image
- HSV thresholding applied
- Binary mask generated

---

## 3. Contour Detection

The largest green contour is detected.

The center coordinates are computed using image moments.

---

## 4. Error Calculation

Horizontal error is calculated:

```text
error = object_center_x - image_center_x
```

---

## 5. P-Controller

Angular velocity:

```text
angular_z = -Kp × error
```

This rotates the robot toward the object.

---

## 6. Forward Motion

If alignment error is sufficiently small:
- robot moves forward
- continues tracking target

---

## 7. Recovery Logic

If object disappears:
- robot rotates slowly
- searches for object again
- resumes tracking when detected

---

## 8. Obstacle Distance Detection

LiDAR scan data is used to:
- estimate distance
- stop robot near object

---

# Results

The TurtleBot3 successfully:
- detected green object
- aligned using P-controller
- followed target autonomously
- stopped near object using LiDAR data


---

# Detailed File Structure

```text
ros2_color_navigation/
│
├── README.md
│
├── .gitignore
│
├── screenshots/
│   ├── gazebo_simulation.png
│   ├── camera_feed.png
│   ├── green_mask.png
│   ├── object_following.png
│   └── terminal_output.png
│
├── ros2_ws_pri/
│   │
│   ├── build/
│   │
│   ├── install/
│   │
│   ├── log/
│   │
│   └── src/
│       │
│       ├── color_navigation/
│       │   │
│       │   ├── package.xml
│       │   │
│       │   ├── setup.py
│       │   │
│       │   ├── setup.cfg
│       │   │
│       │   ├── resource/
│       │   │   └── color_navigation
│       │   │
│       │   ├── color_navigation/
│       │   │   │
│       │   │   ├── __init__.py
│       │   │   │
│       │   │   └── color_follower.py
│       │   │
│       │   └── test/
│       │       ├── test_copyright.py
│       │       ├── test_flake8.py
│       │       └── test_pep257.py
│       │
│       └── tb3_custom_world/
│           │
│           ├── package.xml
│           │
│           ├── setup.py
│           │
│           ├── setup.cfg
│           │
│           ├── resource/
│           │   └── tb3_custom_world
│           │
│           ├── tb3_custom_world/
│           │   └── __init__.py
│           │
│           ├── launch/
│           │   └── green_sphere_world.launch.py
│           │
│           ├── worlds/
│           │   └── green_sphere_world.world
│           │
│           └── test/
│               ├── test_copyright.py
│               ├── test_flake8.py
│               └── test_pep257.py
│
└── videos/
    └── demo_video_link.txt
```
---

# Learning Outcomes

This project demonstrates:

- ROS2 Publisher/Subscriber communication
- OpenCV image processing
- HSV color segmentation
- Contour detection
- Real-time robotic perception
- Autonomous navigation
- P-controller implementation
- Gazebo simulation
- LiDAR integration
- Git and GitHub workflow

---

# Future Improvements

- PID controller implementation
- Multi-object tracking
- Dynamic obstacle avoidance
- SLAM integration
- YOLO object detection
- Real robot deployment

---

# Author

## Priyanshu Mohanty

GitHub:
https://github.com/priyanshum2142

---

# License

This project is licensed under the MIT License.
