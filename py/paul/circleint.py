#circle intersection pts
from __future__ import (division)
import math

def distance (a,b,c,d):
	q = ((a - c)**2 +(b-d)**2 )**0.5
	return q

a,b,c,d = map(int,raw_input().split())
r, s  = map(int,raw_input().split())
#if TRUE == TRUE  #((r+s > D) or D > math.abs(r0-r)	)
#                #else
D = ((a - c)**2 +(b-d)**2 )**0.5
delta = (1/4)*(((D+r+s)*(D+r-s)*(D-r+s)*(-D+r+s))**0.5)
x1 = ((a+c)/2) + (((c-a) * (r**2 - s**2))/(2*(D**2))) + (2*((b-d)*delta)/D) 
x2 = ((a+c)/2) + (((c-a) * (r**2 - s**2))/(2*(D**2))) - (2*((b-d)*delta)/D) 
y1 = ((b+d)/2) + (((d-b) * (r**2 - s**2))/(2*(D**2))) + (2*((b-d)*delta)/D) 
y2 = ((b+d)/2) + (((d-b) * (r**2 - s**2))/(2*(D**2))) - (2*((a-c)*delta)/D) 
#if((diatance() != )and(diatance() != ) ){
#	x1,y1,x2,y2 = x2,y1,
print "x1 = %f" %x1
print "x2 = %f" %x2
print "y1 = %f" %y1
print "y2 = %f" %y2

# after here compare with point 3 in the tri alteration and select the point that is nearer to the third beacon



