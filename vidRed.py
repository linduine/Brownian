#this is the first part of my Brownian project. This snippet is almost entirely based - 
# with minor alterations on examples of CV HoughCircles that circulate on the web.
#This part detects moleculae and stores coordinates with radii to json file, 
#to be processed and modelled with d3.js
#Currently I'm working only with the first video of Browninan motion that was recorded
#at the Summer School of Russian Reporter (Russian news weekly). There are three of them, 
#and both this part and follow ups would be altered to fit them as well.
#Current version of 6 Aug 2014

import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import numpy as np
import collections
import sched
import itertools
import time
import json
import cv2

objects = {}
cap = cv2.VideoCapture('one.avi')
#cap.set(6, 1);
j = open("data.json","wb")

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #insert a timer here
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,50,
                        param1=50,param2=1,minRadius=0,maxRadius=10)
    if circles is not None:
        nframe = time.time()
    	circles = np.uint16(np.around(circles.astype(np.double),3))
        merged = list(itertools.chain.from_iterable(circles.tolist()))
        objects[str(nframe)] = {'Time': str(nframe), 'Moleculae': merged}
        #json.dump(objects, j)
        #j.flush()

    	for i in circles[0,:]:
    	# draw the outer circle
    		cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
    	# draw the center of the circle
    		cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)
    cv2.imshow('frame',gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
json_str = json.dumps(objects, sort_keys=True, indent=2)
print json_str
j.write(json_str)
j.close()
print "JSON report written"
cap.release()
cv2.destroyAllWindows()
print "Program finished"