"""/*
 	author Tara
*/"""

import socket
import multiprocessing as mp
import datetime
import sys
import time
import random
from threading import Thread
import pickle
class Monitor:                                    #UDP server, receive and display all the state of the Philosopher
	def __init__(self):
		self.host =socket.gethostname()
		self.port = 6543
		self.udpserver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #create udp server socket
		self.udpserver_socket.bind((self.host,self.port))
		print("Author: Tara Prasad Bhattarai\n")
		title = []
		title.append("Current Time      ")         #To print the 5 title of Philosopher
		for i in range(1,6):
			title.append("Philosopher "+str(i))
		print("\t\t".join(map(str,title)))
		#print2018-04-20 11:54:45
	def start(self):      				#start the UDP server
		while 1:
			message,address = self.udpserver_socket.recvfrom(1024)   #receive the message from udp client and store the message in "message"
			th =Thread(target = self.displayReceiveData, args=(message,))
			th.start()

		
	def displayReceiveData(self,data):     #Display the state of each Philosopher send by philosopher through udp socket
		philo_state = []
		rdata = pickle.loads(data)
		pid = rdata[0]
		state = rdata[1]
		philo_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')    #To display the current time of each event
		philo_state.append(philo_time)
		
		for i in range(1,6):           # Concatenate state of philosopher and print
			if i == pid:
				philo_state.append(state)
			else:
				philo_state.append("--------")
		print('\t\t'.join(map(str,philo_state)))          #

if __name__=="__main__":
	monitor = mp.Process(target = Monitor().start, args = ())
	monitor.daemon=True	
	monitor.start() 
	time.sleep(95)                     # Determine the Program life
	monitor.terminate()
