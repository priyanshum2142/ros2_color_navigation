import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/priyanshu/ros2_ws_pri/install/tb3_custom_world'
