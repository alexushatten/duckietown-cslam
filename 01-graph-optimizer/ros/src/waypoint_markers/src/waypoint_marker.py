#!/usr/bin/env python
import rospy
import interactive_markers
from interactive_markers.interactive_marker_server import *
from visualization_msgs.msg import *
from duckietown_msgs.msg import Pose2DStamped


class WayPointNode():
    def __init__(self):
        rospy.init_node("waypoint_marker")
        # create an interactive marker server on the topic namespace simple_marker
        self.server = InteractiveMarkerServer("waypoint_marker")

        self.interactive_marker = self.create_interactive_marker()
        self.marker = self.create_marker()
        self.box_control = self.create_box_control()
        self.box_control.markers.append(self.marker)
        
        # add the control to the interactive marker
        self.interactive_marker.controls.append(self.box_control)

        self.control_xaxis = self.move_xaxis()
        self.control_yaxis = self.move_yaxis()

        # add the control to the interactive marker
        self.interactive_marker.controls.append(self.control_xaxis)
        self.interactive_marker.controls.append(self.control_yaxis)

        # init the destination publisher
        self.destionation_publisher = rospy.Publisher("~destination_coordinates", Pose2DStamped, queue_size = 1)
        
        

        # add the interactive marker to our collection &
        # tell the server to call processFeedback() when feedback arrives for it
        self.server.insert(self.interactive_marker, self.processFeedback)

        self.server.applyChanges()

    def create_box_control (self):
        # create a non-interactive control which contains the box
        box_control = InteractiveMarkerControl()
        box_control.always_visible = True
        return box_control

    def create_interactive_marker(self):
        # create an interactive marker for our server
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = "map"
        int_marker.name = "marker"
        return int_marker

    def create_marker(self):
        # create a duckie marker
        marker = Marker()

        marker.header.frame_id = "/map"
        marker.ns = "duckie"

        marker.type = marker.MESH_RESOURCE
        marker.action = marker.ADD
        marker.mesh_resource = "package://duckietown_visualization/meshes/others/duckie.dae"
        marker.mesh_use_embedded_materials = True

        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        return marker
    
    def move_xaxis (self):
        # create a control which will move the box
        control = InteractiveMarkerControl()
        control.name = "move_x"
        control.orientation.w = 1
        control.orientation.x = 1
        control.orientation.y = 0
        control.orientation.z = 0
        control.always_visible = False
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        return control

    def move_yaxis (self):
        # create a control which will move the box
        control = InteractiveMarkerControl()
        control.name = "move_y"
        control.orientation.w = 1
        control.orientation.x = 0
        control.orientation.y = 0
        control.orientation.z = 1
        control.always_visible = False
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        return control
    

    def processFeedback(self, feedback):
        msg = Pose2DStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.header.frame_id = "map"
        msg.x = feedback.pose.position.x
        msg.y = feedback.pose.position.y
        self.destionation_publisher.publish(msg)

if __name__ == '__main__':
    # Initialize the node
    waypoint_node = WayPointNode()
    # Keep it spinning to keep the node alive
    rospy.spin()