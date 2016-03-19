from __future__ import division
import requests
import random
import time
import threading
import rethinkdb as r
import math
import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from scipy.misc import imread

import os

plt.scatter([0,5],[0,5])
plt.ion()
plt.show()
plt.clf()
plt.gca().grid(1)
img = imread("im1.png")
plt.imshow(img,zorder = 0, extent=[-1,4, -8, 3.5])

# Coordinates of the Beacons
x = [0,0,3,3,1.5]
y = [0,3,0,3,1.5]
# End Segment
maximum =10

#init fences
FENCES = []
for i in xrange(0,3):
	for j in xrange(0,3):
		FENCES+=[[[i,j],[i,j+1],[i+1,j+1],[i+1,j]]]

def kmeans(Z,STO):# pg please make Z a np array like the one described below :P
	#Z = np.array([[a1,b1],[x1,y1],[x2,y2],[a3,b3],[a2,b2]])
	# convert to np.float32
	# plt.clf()
	Z = np.float32(Z)
	# define criteria and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,1,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
	# pls add corresponding entries for each cluster
	# Now separate the data, Note the flatten()
	A = Z[label.ravel()==0]
	B = Z[label.ravel()==1]

	# Plot the data
	#""" 
	#rempove for debug 
	plt.scatter(A[:,0],A[:,1])
	plt.scatter(B[:,0],B[:,1],c = 'r')
	plt.scatter([x[1],x[2],x[3],x[0],x[4]],[y[1],y[2],y[3],y[0],y[4]],s = 40, c = 'red')
	plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')
	plt.xlabel('X'),plt.ylabel('Y')
	plotfences(plt)
	plt.draw()
	pt = [center[:,0],center[:,1]]
	print(checkfences(pt))

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
	
	r =[random.random()*1,random.random()*4,random.random()*4,random.random()*5,random.random()*2.5]


	# Hardcoded beacon data end
	# END OF FUNCTION DECLARITIONS

	alive = 5
	nclusters = 2
	PTS = []
	#taking groups of 3
	for i in range(0,alive-2):
		for j in range(i+1,alive-1):
			for k in range(j+1,alive):
				PTS = PTS + Intersects(x[i],y[i],x[j],y[j],x[k],y[k],r[i],r[j],r[k])
				#print i,j
				PTS = PTS + Intersects(x[i],y[i],x[k],y[k],x[j],y[j],r[i],r[k],r[j])
				#print j,k
				PTS = PTS + Intersects(x[j],y[j],x[k],y[k],x[i],y[i],r[j],r[k],r[i])
				#print k,i
	#"""
	STO = []
	CentreWeight = 10000000000000
	#print STO
	#print PTS
	kmeans(np.array(PTS),np.array(STO))

def checkfences(pt): # ref to global variable FENCES
	for i in range(0,len(FENCES)):
		if(infence(FENCES[i],pt)):
			return i
	return -1

def getDistance(rssi, txPower):  
    return pow(10, ( txPower - rssi) / (10 * ATTN))

"""
fence1 = [[0,0],[0,1],[1,1],[1,0]] # define points in the order of loop
point1 = [1.05,1]
point2 = [2,2]
infence(fence1,point1)
"""
def infence(fence,pt): 
	bbPath = matplotlib.path.Path(np.array(fence))
	return bbPath.contains_point((pt[0], pt[1]))	

def plotfences(media):
	for i in range(0,len(FENCES)):
		rectangle = media.Rectangle((FENCES[i][0][0],FENCES[i][0][1]), 1, 1, fc='None')
		media.gca().add_patch(rectangle)

def postdata(segment,x,y):
	r=requests.post(IpAddress, data = {"segment":segment ,"x":x, "y":y})


# main Begins Here
while(1):
	time.sleep(0.01)
	display_data()