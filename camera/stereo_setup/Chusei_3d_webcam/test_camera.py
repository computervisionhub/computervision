#! /usr/bin/env python
 
import numpy as np
import cv2
import os
import rospy
import shlex
import subprocess
import yaml
import thread

class LittleStereoCam():
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cam_id=0
        self.cam=cv2.VideoCapture(cam_id)
        # rospy.loginfo(self.left_yaml_file)
        #'''
        ret,frame=self.cam.read()
        while not ret:
            print('[ERROR]: frame error')
            rospy.sleep(0.2)
            ret,frame=self.cam.read()
        #'''
        cam_mode_dict={
            'LEFT_EYE_MODE':1,
            'RIGHT_EYE_MODE':2,
            'RED_BLUE_MODE':3,
            'BINOCULAR_MODE':4,
            }
        cam_mode=cam_mode_dict['BINOCULAR_MODE']
        command_list=[
 
 
        "uvcdynctrl -d /dev/video{cam_id} -S 6:8 '(LE)0x50ff'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:15 '(LE)0x50f6'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:8 '(LE)0x2500'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:8 '(LE)0x5ffe'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:15 '(LE)0x0003'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:15 '(LE)0x0002'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:15 '(LE)0x0012'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:15 '(LE)0x0004'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:8 '(LE)0x76c3'",
        "uvcdynctrl -d /dev/video{cam_id} -S 6:10 '(LE)0x0{cam_mode}00'",
 
        ]
 
        for command in command_list:
            subprocess.Popen(shlex.split(command.format(cam_id=cam_id,cam_mode=cam_mode)))

    def run(self):
        while True:
            ret,frame=self.cam.read()
            if not ret:
                print('[ERROR]: frame error')
                break            
            expand_frame=cv2.resize(frame,None,fx=2,fy=1)# scale the img
            
            cv2.imshow("frame", frame)
            cv2.waitKey(10)

 
if __name__ == '__main__':
    lsc = LittleStereoCam()
 
    try:
        lsc.run()
    except rospy.ROSInterruptException:
        pass
