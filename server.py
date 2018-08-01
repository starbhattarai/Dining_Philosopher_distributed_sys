"""/*
 	author Tara
*/"""
import socket
import multiprocessing as mp
import datetime
import sys
import time
import random
import pickle
from threading import Thread
class Fork:
	def __init__(self):
		self.state="Free"
		self.host= socket.gethostname()
		
	def connection(self,port):         #TCP Socket for Server i.e Forks
		self.port = port
		self.sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket for fork
		self.sockt.bind((self.host, self.port)) #bind the socket to host and port
		self.sockt.listen(2)    #server listen for the client request in the bind port
		while True:
			newsocket, client_addr = self.sockt.accept()    #this written pairs of address is new socket object 
									#usable to send and receive data on the connection and 
									#address is the address binded to the socket on the other end
			th = Thread(target=self.sendMessageToClient, args=(newsocket, client_addr))
			th.start()
		
	def sendMessageToClient(self, newsocket, client_addr):
		while 1:
			try:
				req_data = pickle.loads(newsocket.recv(4096))    #receive data from client
				if req_data:
					if(req_data == "request" and self.state == "Busy"): #if fork is used by next philosopher, this philosopher
						time.sleep(random.randint(1,3))                               #will stay in a queue for 1 to 2 sec
					if(req_data == "request" and self.state == "Free"):  #Enter to the critical section
						self.state = "Busy"                          #set flags to Busy
						newsocket.send(pickle.dumps("Free", -1))	# Inform client that fork is available
						time.sleep(1)
						release_data = pickle.loads(newsocket.recv(4096))  # Get release signal from the philosopher and 
						if release_data == "release":			   # and set the flags to Free again
							self.state = "Free"
					else:
						newsocket.send(pickle.dumps("Busy", -1))	

			except:
				break
		newsocket.close()



if __name__ == "__main__":
	try:
		number_of_forks = 5
		fork_address = [4250+i for i in range(5)]     #list of ports where five forks run   4250+i for i in range(5)
		fork_num = [1,2,3,4,5]
		#f1 = Fork()
		fork_process = []
		for i in range(number_of_forks):            #create five forks
			fork = mp.Process(target = Fork().connection, args = (fork_address[i],))
			fork_process.append(fork)
			fork.start()                        #start five forks
		time.sleep(100)
		#for fork in fork_process:
		#fork.join()
		for fork in fork_process:		   #terminate five forks after 100 sec
			fork.terminate()
	except KeyboardInterrupt: 
		sys.exit()


