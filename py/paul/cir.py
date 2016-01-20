"""
/**
 * Finds the intersections of two circles, if they exist.
 *
 * Given two circle equations:
 *   Cirlce 1: r1^2 = (x - x1)^2 + (y - y1)^2
 *   Circle 2: r2^2 = (x - x2)^2 + (y - y2)^2
 *
 * Returns coordinates (2 sets of 2 doubles) or else returns null if intersections do not exist.
 *
 * Rarely this function may return null if the circles are tangental or very close to tangental.
 */
"""

from __future__ import (division)
import math

def Intersects(x1,y1,x2,y2,x3,y3,r1,r2,r3):
	
	#Cirlce 1: r1^2 = x^2 + y^2
	#Circle 2: r2^2 = (x - a)^2 + (y - b)^2
	
	a = x2 - x1;
	b = y2 - y1;
	
	#// Find distance between circles.
	d = math.sqrt(a*a + b*b);
	
	#// Ensure that the combined radii lengths are longer than the distance between the circles,
	#// i.e. tha the circles are close enough to intersect.
	if (r1 + r2 <= d):
		 sx1,sy1,sx2,sy2 = ((x1+x2)/2),((y1+y2)/2),((x1+x2)/2),((y1+y2)/2)
	#// Ensure that one circle is not inside the other.
	elif (d <= abs( r1 - r2 )):
		sx1,sy1,sx2,sy2 = ((x1+x2)/2),((y1+y2)/2),((x1+x2)/2),((y1+y2)/2)
	#Calculate

	#// Find the intersections (formula derivations not shown here).
	else:
		t = math.sqrt( (d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (-d + r1 + r2) )

		sx1 = 0.5 * (a + (a*(r1*r1 - r2*r2) + b*t)/(d**2))
		sx2 = 0.5 * (a + (a*(r1*r1 - r2*r2) - b*t)/(d**2))

		sy1 = 0.5 * (b + (b*(r1*r1 - r2*r2) - a*t)/(d**2))
		sy2 = 0.5 * (b + (b*(r1*r1 - r2*r2) + a*t)/(d**2))

		#// Translate to get the intersections in the original reference frame.
		sx1 = sx1 + x1
		sy1 = sy1 + y1
		sx2 = sx2 + x1
		sy2 = sy2 + y1
	
	#ox = sx1 
	#oy = sy1
	#if(math.sqrt((sx1-x3)**2 + (sy1-y3)**2)>math.sqrt((sx2-x3)**2 + (sy2-y3)**2)) :
	#	ox = sx2 
	#	oy = sy2
	
	print "a1 = %f" %x1
	print "b1 = %f" %y1
	print "a2 = %f" %x2
	print "b2 = %f" %y2
	print "a3 = %f" %x3
	print "b3 = %f" %y3
	print "x1 = %f" %sx1
	print "y1 = %f" %sy1
	print "x2 = %f" %sx2
	print "y2 = %f" %sy2




a,b,c,d,e,f = map(float,raw_input().split())
#print a,b,c,d
r, s,t  = map(float,raw_input().split())
Intersects(a,b,c,d,e,f,r,s,t)

#      ellipse( s[0], s[1], 8, 8 );
#      ellipse( s[2], s[3], 8, 8 );

