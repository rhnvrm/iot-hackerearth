from __future__ import division
import random
import time
import threading
import rethinkdb as r
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
import requests as r

plt.scatter([0,5],[0,5])
plt.ion()
plt.show()
plt.clf()
plt.gca().grid(1)

# Coordinates of the Beacons
x1=0
y1=0
x2=8
y2=0
x3=4
y3=3
# End Segment
maximum =10

fences = [[1,1,1,2,2,2,2,1],[0,0,0,0,0,0,0,0]]

def kmeans(Z,STO):# pg please make Z a np array like the one described below :P
	#Z = np.array([[a1,b1],[x1,y1],[x2,y2],[a3,b3],[a2,b2]])
	# convert to np.float32
	# plt.clf()
	Z = np.float32(Z)
	# define criteria and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,1,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
	# pls add corresponding entries for each cluster
	# Now separate the data, Note the flatten()
	A = Z[label.ravel()==0]
	B = Z[label.ravel()==1]

	# Plot the data
	#""" 
	#rempove for debug 
	plt.scatter(A[:,0],A[:,1])
	plt.scatter(B[:,0],B[:,1],c = 'r')
	plt.scatter([x1,x2,x3],[y1,y2,y3],s = 40, c = 'red')
	plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')
	plt.xlabel('X'),plt.ylabel('Y')
	plt.draw()
	#plt.show()
	#"""
	STO = center

def Intersects(x1,y1,x2,y2,x3,y3,r1,r2,r3):
	#Cirlce 1: r1^2 = x^2 + y^2
	#Circle 2: r2^2 = (x - a)^2 + (y - b)^2
	a = x2 - x1;
	b = y2 - y1;
	d = math.sqrt(a*a + b*b);
	if (r1 + r2 <= d):
		 sx1,sy1,sx2,sy2 = ((x1+x2)/2),((y1+y2)/2),((x1+x2)/2),((y1+y2)/2)
	elif (d <= abs( r1 - r2 )):
		sx1,sy1,sx2,sy2 = ((x1+x2)/2),((y1+y2)/2),((x1+x2)/2),((y1+y2)/2)
	else:
		t = math.sqrt( (d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (-d + r1 + r2) )

		sx1 = 0.5 * (a + (a*(r1*r1 - r2*r2) + b*t)/(d**2))
		sx2 = 0.5 * (a + (a*(r1*r1 - r2*r2) - b*t)/(d**2))

		sy1 = 0.5 * (b + (b*(r1*r1 - r2*r2) - a*t)/(d**2))
		sy2 = 0.5 * (b + (b*(r1*r1 - r2*r2) + a*t)/(d**2))

		sx1 = sx1 + x1
		sy1 = sy1 + y1
		sx2 = sx2 + x1
		sy2 = sy2 + y1
#	if take set with min abs error from dist from the 3rd side
	
	if (abs((((sx1-x3)**2 +(sy1-y3)**2)**0.5)-r3)>=abs((((sx2-x3)**2 +(sy2-y3)**2)**0.5)-r3)):
		return [[sx2,sy2]]
	else:
		return [[sx1,sy1]]
	"""	
	#append the following to the storing array that passes to the kmeans clustering
	print "x1 = %f" %sx1
	print "y1 = %f" %sy1
	print "x2 = %f" %sx2
	print "y2 = %f" %sy2
	#[sx1,sy1,sx2,sy2]
	return [[sx1,sy1],[sx2,sy2]]
	"""

def display_data():
	# hardcoded beacon data Start
	
	r1,r2,r3 = 	5+random.random(),5+random.random(),5+random.random()


	# Hardcoded beacon data end
	# END OF FUNCTION DECLARITIONS

	alive = 3
	nclusters = 2
	PTS = []
	#taking groups of 3
	for i in range(0,alive-2):
		for j in range(i+1,alive-1):
			for k in range(j+1,alive):
				PTS = PTS + Intersects(x1,y1,x2,y2,x3,y3,r1,r2,r3)
				#print i,j
				PTS = PTS + Intersects(x1,y1,x3,y3,x2,y2,r1,r3,r2)
				#print j,k
				PTS = PTS + Intersects(x2,y2,x3,y3,x1,y1,r2,r3,r1)
				#print k,i
	#"""
	STO = []
	CentreWeight = 10000000000000
	#print STO
	#print PTS
	kmeans(np.array(PTS),np.array(STO))

def getDistance(rssi, txPower):  
    return pow(10, ( txPower - rssi) / (10 * ATTN))

def infence(fence,pt): 
	bbPath = matplotlib.path.Path(np.array([[fence[0], fence[1]],[fence[2], fence[3]],[fence[4], fence[5]],[fence[6], fence[7]]]))
	return bbPath.contains_point((pt[0], pt[1]))	

while(1):
	display_data()
	time.sleep(0.01)

