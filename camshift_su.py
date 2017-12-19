#!/usr/bin/env python

'''
Camshift tracker
================

This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

http://www.robinhewitt.com/respearch/track/camshift.html

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

import numpy as np
import cv2
import logging
import urllib2
import time
import json

import video
import config

logging.basicConfig(format='%(asctime)s,%(msecs)-3d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('fuming')

# cv.CV_FOURCC('M','J','P','G')
# cv2.cv.CV_FOURCC('X', 'V', 'I', 'D')


lastSecond = -1
tmpFileName = "temp.avi"
lastFileName = tmpFileName
currentStatus = 'close'

videoWriter = cv2.VideoWriter(
    lastFileName, cv2.cv.CV_FOURCC('X', 'V', 'I', 'D'), 10, (640, 480), True)


def refresphVideo(fileName):
    global videoWriter
    videoWriter.release()
    if currentStatus == 'close':
        videoWriter = cv2.VideoWriter(tmpFileName, cv2.cv.CV_FOURCC(
            'X', 'V', 'I', 'D'), 10, (640, 480), True)
    else:
        fileName = fileName + ".avi"
        logger.debug(fileName)
        videoWriter = cv2.VideoWriter(fileName, cv2.cv.CV_FOURCC(
            'X', 'V', 'I', 'D'), 10, (640, 480), True)


class Camera(object):

    def __init__(self, video_src):
        self.cam = video.create_capture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False

    def run(self):
        global currentStatus, lastFileName, videoWriter, lastSecond
        while True:
            _current_second = int(time.strftime("%S", time.localtime()))
            if _current_second != lastSecond:
                f = open("cHello.ini")
                resp = json.loads(f.readline())
                f.close()
                logger.debug(resp)
                if resp['status'] != currentStatus:
                    currentStatus = resp['status']
                    refresphVideo(resp['fileName'])
                if resp['fileName'] != lastFileName:
                    refresphVideo(resp['fileName'])
                    lastFileName = resp['fileName']
                lastSecond = _current_second
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()
            if currentStatus == 'open':
                cv2.putText(vis, "RECORD...", (10, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2, False)
                videoWriter.write(self.frame)
            else:
                cv2.putText(vis, "NOT RECORD...", (10, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2, False)
            cv2.imshow('camshift', vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
            # time.sleep(0.05)
        videoWriter.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    print __doc__
    resp = '{"status":"' + currentStatus + \
        '","fileName":"' + tmpFileName + '"}'
    f = open("cHello.ini", "w")
    f.write(resp)
    f.close()
    _g_Camera = Camera(video_src)
    _g_Camera.run()
