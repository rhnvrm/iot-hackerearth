from __future__ import division

import threading
import rethinkdb as r

import os

conn = r.connect( "localhost", 28015 , db='heck')

ATTN = 2

def getDistance(rssi, txPower):
    
    return pow(10, ( txPower - rssi) / (10 * ATTN))


power_to_A_lookup_table = {"B4:99:4C:57:AE:E3": -71, "B4:99:4C:57:D2:AA": -71, "B4:99:4C:57:EC:C6": -71}
distance_lookup_table = {"B4:99:4C:57:AE:E3": -1, "B4:99:4C:57:D2:AA": -1, "B4:99:4C:57:EC:C6": -1}
#old_distance_lookup_table = {"B4:99:4C:57:AE:E3": -1, "B4:99:4C:57:D2:AA": -1, "B4:99:4C:57:EC:C6": -1}

x = {u'old_val': {u'uid': u'B4:99:4C:57:EC:C6', u'rssi': -61, u'name': u'Bluetooth Device', u'timestamp': 1453011839.46865}, u'new_val': {u'uid': u'B4:99:4C:57:EC:C6', u'rssi': -55, u'name': u'Bluetooth Device', u'timestamp': 1453011857.281005}}


def print_distance_lookup_table():
	#something = something + 1 #lol


	#os.system('cls' if os.name == 'nt' else 'clear')

	for i in distance_lookup_table:
		print str(i) + " -> " + str(distance_lookup_table[i])# + " ( Difference: " + str(distance_lookup_table[i] - old_distance_lookup_table[i]) + " )"

feed = r.table('beacons').changes().run(conn)
for change in feed:
	if change['new_val']['uid']  in  power_to_A_lookup_table:
		#old_distance_lookup_table = distance_lookup_table
		distance_lookup_table[change['new_val']['uid']]  = 	getDistance(int(change['new_val']['rssi']), power_to_A_lookup_table[change['new_val']['uid']])
		
		#for i in distance_lookup_table:
			#print "here\n"
		#	print str(i) + " -> " + str(distance_lookup_table[i])

		t=threading.Thread(target=print_distance_lookup_table)
		t.daemon = True
		t.start()


