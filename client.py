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
class Philosopher:
	def __init__(self,pid,host,fork1_port, fork2_port):
		self.pid = pid
		
		self.host = socket.gethostbyname(host)           #Provide Fork server ip_address to the Philosopher
		self.udp_host =socket.gethostbyname(sys.argv[2]) #Provide Monitor server ip_address to Philosopher
		self.fork1_port=fork1_port		         #Assign first fork
		self.fork2_port=fork2_port		         #Assign second fork
		self.fork1 = fork1_port
		self.fork2 = fork2_port

	def forkcheck(self,fork_port):  		#create TCPSocket and checke whether given fork is availabel or not?
		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientsocket.connect((self.host, fork_port))
		clientsocket.send(pickle.dumps("request", -1))   #Send a "request" signal to the fork if fork is Free it will
		data = pickle.loads(clientsocket.recv(4096))     #send back a "Free" signal to Philosopher
		#Store a received signal i.e data and client socket handle 
		listdata = [data,clientsocket]
		
		return listdata

	def changeState(self):          # Change the Philosopher form one state to another
		while 1:	
			self.sendState(self.pid,self.udp_host,"Thinking")#print("Thinking"+str(self.pid)) # Print thinking state
			time.sleep(random.randint(1,5))     #Philosopher becomes hungry after random time between 1 to 5 sec
			self.eating()
		
	def eating(self):
		self.sendState(self.pid,self.udp_host,"Hungry  ")#print("Hungry"+str(self.pid))          #Hungry state
		rec_listdata1 = self.forkcheck(self.fork1_port)   #Try to acquire a first fork,It checks whether fork 1 is available or not?
		rec_listdata2 = self.forkcheck(self.fork2_port)   #Try to acquire a second fork, It checks whether fork 2 is available or not?
		if (rec_listdata1[0] == "Free" and              #Philosopher Enter to the eating state
			 rec_listdata2[0] == "Free"):
			self.sendState(self.pid,self.udp_host,"Eating  ")#print("Eating"+str(self.pid))	
			time.sleep(random.randint(1,3))
			rec_listdata1[1].send(pickle.dumps("release",-1)) #Release fork 1 after eating
			rec_listdata2[1].send(pickle.dumps("release",-1)) #Release fork 2 after eating
			self.sendState(self.pid,self.udp_host,"Thinking")   #new
			time.sleep(random.randint(3,10))	   # 
			#rec_listdata1[1].close()
			#rec_listdata2[1].close()
		elif(rec_listdata1[0] == "Busy" and rec_listdata2[0]=="Free"): # if fork 1 is not availabel, release fork 2
			rec_listdata2[1].send(pickle.dumps("release",-1))
		elif(rec_listdata1[0] == "Free" and rec_listdata2[0]=="Busy"): #if fork 2 is not available, release fork 1
			rec_listdata2[1].send(pickle.dumps("release",-1))
		rec_listdata1[1].close()
		rec_listdata2[1].close()
#################################
	def sendState(self,pid,udp_host,message):               # UDP client, will send the status of each process to Monitor
		state = pickle.dumps([self.pid, message])
		udpclt_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udpclt_socket.sendto(state,(self.udp_host,6543))     #send the message to server host and server port
									#is it necessary to have receive here?
		udpclt_socket.close()
#################################



if __name__=="__main__":
	number_of_philo = 5
	fork_address = [4250+i for i in range(5)]       #4250+i for i in range(5)   
	philo_num = [1,2,3,4,5]
	philo_process = []
	for i in range(number_of_philo):    #create five philosophers
		philo = mp.Process(target = Philosopher(philo_num[i],sys.argv[1],      #assign philosopher number, fork_ipaddress,fork1_address, 
			fork_address[i],fork_address[(i+1)%5]).changeState, args = ()) #fork2_address
		philo_process.append(philo)
		philo.daemon=True		
		philo.start()               #start five philosophers    
	   
	time.sleep(90)                     #Determine how long philosopher runs
	#for philo in philo_process:
		#philo.join()
	for philo in philo_process:        #terminate five philosophers
		philo.terminate()


