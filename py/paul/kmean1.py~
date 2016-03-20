import numpy as np
import cv2
from matplotlib import pyplot as plt
#X = np.array([[1,1],[2,1],[3,1],[4,1],[5,1],[6,1]])
#Y = np.array([[1,2],[1,3],[1,4],[1,5],[1,6],[1,7]])
#X = np.random.randint(25,500,(50,2))
#print (X)
#Y = np.random.randint(23,450,(50,2))
#print Y
#Z = np.vstack((X,Y))
#print Z
#Z = np.array([[1,1],[2,1],[3,1],[4,1],[5,1],[6,1]])
#Z = np.array([[0.133974596216,1.5],[1.86602540378,0.633974596216]])

"""
a1 = 0.000000
b1 = 1.000000
a2 = 1.000000
b2 = 0.000000
a3 = 2.000000
b3 = 2.000000
x1 = 0.000000
y1 = 0.000000
x2 = 1.000000
y2 = 1.000000
"""
x1=0
y1=0
x2=8
y2=0
x3=4
y3=3

#Z = np.array([[a1,b1],[x1,y1],[x2,y2],[a3,b3],[a2,b2]])
# convert to np.float32
a=raw_input()
b=raw_input()
Z = np.array([[a,b],[a,b],[a,b]])
Z = np.float32(Z)
# define criteria and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret,label,center=cv2.kmeans(Z,1,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now separate the data, Note the flatten()
#A = Z[label.ravel()==0]
#B = Z[label.ravel()==1]
#C = Z[label.ravel()==2]
#B = Z[label.ravel()==1]

# Plot the data
plt.xlim(-3, 11)
plt.ylim(-5, 10)
plt.scatter([x1,x2,x3],[y1,y2,y3],s = 40, c = 'red')
#plt.scatter(A[:,0],A[:,1],c = 'green')
#plt.scatter(B[:,0],B[:,1],c = 'yellow')
#plt.scatter(C[:,0],C[:,1],c = 'black')
print center
plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')
plt.xlabel('Height'),plt.ylabel('Weight')
plt.show()
#plt.savefig(c+'.png')
