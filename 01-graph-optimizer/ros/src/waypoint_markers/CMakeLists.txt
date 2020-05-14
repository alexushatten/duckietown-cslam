cmake_minimum_required(VERSION 3.0.2)
project(waypoint_markers)

find_package(catkin REQUIRED COMPONENTS interactive_markers roscpp visualization_msgs tf)

catkin_package(
  CATKIN_DEPENDS interactive_markers roscpp visualization_msgs tf duckietown_visualization
)
include_directories(include
  ${catkin_INCLUDE_DIRS}
)

catkin_python_setup()

catkin_package(CATKIN_DEPENDS interactive_markers)

install(PROGRAMS
  src/waypoint_marker.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
