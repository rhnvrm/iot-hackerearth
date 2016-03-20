"""
	Bluetooth Indoor Positioning
			- Paul George && Rohan Verma	
"""
from __future__ import (division)
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
# hardcoded beacon data Start
x1=0
y1=0
x2=3.4
y2=0
x3=1.7
y3=1.4
r1=2.818
r2=1.25
r3=0.6309

# Hardcoded beacon data end
def kmeans(Z,STO):# pg please make Z a np array like the one described below :P
	#Z = np.array([[a1,b1],[x1,y1],[x2,y2],[a3,b3],[a2,b2]])
	# convert to np.float32
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
	plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')
	plt.xlabel('Height'),plt.ylabel('Weight')
	plt.show()
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
	#append the following to the storing array that passes to the kmeans clustering
	print "x1 = %f" %sx1
	print "y1 = %f" %sy1
	print "x2 = %f" %sx2
	print "y2 = %f" %sy2
	#[sx1,sy1,sx2,sy2]
	return [[sx1,sy1],[sx2,sy2]]
	
# END OF FUNCTION DECLARITIONS

alive = 4
nclusters = 2
PTS = []
#taking groups of 3
for i in range(0,alive-3):
	for j in range(i+1,alive-2):
		for k in range(j+1,alive-1):
			PTS = PTS + Intersects(x1,y1,x2,y2,x3,y3,r1,r2,r3)
			print i,j
			PTS = PTS + Intersects(x1,y1,x3,y3,x2,y2,r1,r2,r3)
			print j,k
			PTS = PTS + Intersects(x2,y2,x3,y3,x1,y1,r1,r2,r3)
			print k,i
#"""
STO = []
CentreWeight = 10000000000000
#print STO
#print PTS
kmeans(np.array(PTS),np.array(STO))



"""
#for i in STO 
	temp = sum of distances to that center
	if CentreWeight >temp  :
		CenterWeight = temp 
		final = STO[i]
		
plot centre and circle after transform
"""
		
	



