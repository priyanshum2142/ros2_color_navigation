# TurtleBot3 Color Based Navigation using ROS2 and OpenCV

## Overview

This project implements autonomous color-based navigation for TurtleBot3 using ROS2 Humble, OpenCV, and Gazebo simulation.

The robot detects a green sphere using computer vision techniques, aligns itself using a proportional controller, moves toward the object, and stops safely using LiDAR data.

---

# Features

- TurtleBot3 Gazebo Simulation
- Custom Gazebo World with Green Sphere
- OpenCV HSV Color Detection
- Contour Detection and Tracking
- Proportional (P) Controller
- Autonomous Object Following
- Recovery Behavior when Object Lost
- LiDAR-based Obstacle Distance Detection
- ROS2 Publisher/Subscriber Architecture

---

# Technologies Used

- ROS2 Humble Hawksbill
- TurtleBot3
- Gazebo
- OpenCV
- Python
- cv_bridge

---

# System Architecture

Camera Image
↓
OpenCV Processing
↓
HSV Thresholding
↓
Contour Detection
↓
Object Center Detection
↓
Error Calculation
↓
P Controller
↓
cmd_vel
↓
TurtleBot3 Motion

---

# Workspace Structure

```text
ros2_ws_pri/
└── src/
    ├── color_navigation/
    └── tb3_custom_world/
