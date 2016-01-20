from __future__ import division

import threading
import rethinkdb as r
import math
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

plt.scatter([0,5],[0,5])
plt.ion()
plt.show()
plt.clf()

x1=0
y1=0
x2=3.4
y2=0
x3=1.7
y3=1.4

def kmeans(Z,STO):# pg please make Z a np array like the one described below :P
	#Z = np.array([[a1,b1],[x1,y1],[x2,y2],[a3,b3],[a2,b2]])
	# convert to np.float32
	#plt.clf()
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
	#plt.scatter(A[:,0],A[:,1])
#	plt.scatter(B[:,0],B[:,1],c = 'r')
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
	if (abs((((sx1-x3)**2 +(sy1-y3)**2)**0.5)-r3)>=	abs((((sx2-x3)**2 +(sy2-y3)**2)**0.5)-r3)):
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
counter = 0
R1 =[]
R2 =[]
R3 =[]

def display_data(distances):
	# hardcoded beacon data Start
	global R1,R2,R3 
	global counter
	R1[counter],R2[counter],R3[counter] = tuple(distances[i] for i in distances)
	counter =counter +1
	if(counter == 5):
		counter = 0
		r1 = sum(R1)/len(R1)
		R1 = []
		r2 = sum(R2)/len(R2)
		R2 = []
		r3 = sum(R3)/len(R3)
		R3 = []
	# Hardcoded beacon data end
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

def getDistance(rssi, txPower):
    
    return pow(10, ( txPower - rssi) / (10 * ATTN))


def print_distance_lookup_table():
	#something = something + 1 #lol


	os.system('cls' if os.name == 'nt' else 'clear')

	for i in distance_lookup_table:
		print str(i) + " -> " + str(distance_lookup_table[i])# + " ( Difference: " + str(distance_lookup_table[i] - old_distance_lookup_table[i]) + " )"

	#display_data(distance_lookup_table)
	


conn = r.connect( "10.207.86.245", 28015 , db='heck')

ATTN = 2



power_to_A_lookup_table = {"B4:99:4C:57:AE:E3": -71, "B4:99:4C:57:D2:AA": -71, "B4:99:4C:57:EC:C6": -71}
distance_lookup_table = {"B4:99:4C:57:AE:E3": -1, "B4:99:4C:57:D2:AA": -1, "B4:99:4C:57:EC:C6": -1}
#old_distance_lookup_table = {"B4:99:4C:57:AE:E3": -1, "B4:99:4C:57:D2:AA": -1, "B4:99:4C:57:EC:C6": -1}

#x = {u'old_val': {u'uid': u'B4:99:4C:57:EC:C6', u'rssi': -61, u'name': u'Bluetooth Device', u'timestamp': 1453011839.46865}, u'new_val': {u'uid': u'B4:99:4C:57:EC:C6', u'rssi': -55, u'name': u'Bluetooth Device', u'timestamp': 1453011857.281005}}



feed = r.table('beacons').changes().run(conn)
for change in feed:
	if change['new_val']['uid']  in  power_to_A_lookup_table:
		#old_distance_lookup_table = distance_lookup_table
		distance_lookup_table[change['new_val']['uid']]  = 	getDistance(int(change['new_val']['rssi']), power_to_A_lookup_table[change['new_val']['uid']])
		
		#for i in distance_lookup_table:
			#print "here\n"
		#	print str(i) + " -> " + str(distance_lookup_table[i])

		#t=threading.Thread(target=print_distance_lookup_table)
		#d=threading.Thread(target=display_data)
		display_data(distance_lookup_table)
		#d.daemon = True
		#t.daemon = True
		#t.start()
		#d.start()



