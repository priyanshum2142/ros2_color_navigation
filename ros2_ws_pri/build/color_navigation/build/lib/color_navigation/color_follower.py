#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

from cv_bridge import CvBridge

import cv2
import numpy as np


class ColorFollower(Node):

    def __init__(self):

        super().__init__('color_follower')

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.front_distance = 999.0

        self.last_error = 0

        self.get_logger().info("Green Object Follower Started")


    def scan_callback(self, msg):

        front_ranges = msg.ranges[0:20]

        valid_ranges = [r for r in front_ranges if not np.isinf(r)]

        if len(valid_ranges) > 0:
            self.front_distance = min(valid_ranges)


    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # GREEN HSV RANGE

        lower_green = np.array([40, 80, 80])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)

        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        twist = Twist()

        if len(contours) > 0:

            largest_contour = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(largest_contour)

            if area > 500:

                x, y, w, h = cv2.boundingRect(
                    largest_contour
                )

                cx = x + w // 2

                width = frame.shape[1]

                center_x = width // 2

                error = cx - center_x

                self.last_error = error

                # VISUALIZATION

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (cx, y+h//2),
                    5,
                    (0, 0, 255),
                    -1
                )

                cv2.line(
                    frame,
                    (center_x, 0),
                    (center_x, frame.shape[0]),
                    (255, 0, 0),
                    2
                )

                # STOP IF CLOSE

                if self.front_distance < 0.4:

                    twist.linear.x = 0.0
                    twist.angular.z = 0.0

                    self.get_logger().info(
                        "Target Reached"
                    )

                else:

                    # P CONTROLLER

                    Kp = 0.002

                    twist.angular.z = -Kp * error

                    # MOVE FORWARD ONLY IF CENTERED

                    if abs(error) < 50:

                        twist.linear.x = 0.12

                    else:

                        twist.linear.x = 0.0

        else:

            # SEARCH BEHAVIOR

            twist.linear.x = 0.0

            if self.last_error > 0:
                twist.angular.z = -0.3
            else:
                twist.angular.z = 0.3

            self.get_logger().info(
                "Searching for object..."
            )

        self.cmd_pub.publish(twist)

        cv2.imshow("Camera View", frame)

        cv2.imshow("Green Mask", mask)

        cv2.waitKey(1)


def main(args=None):

    rclpy.init(args=args)

    node = ColorFollower()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()