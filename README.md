# Dining_Philosopher_distributed_sys
Program solves the Dining Philosopher Problem in Distributed system

*Philosopher has 3 state:
	Thinking
	Hungry
	Eating
*Fork has 2 state:
	Free
	Busy
Philosopher, Fork and Monitor run in different 3 hosts
Philosopher,client, communicate with Fork,server, with the help of TCP socket and
Philosopher communicate with Monitor which is another server with the help of 
UDP socket

Each time Philosopher wants to eat it has to access two forks,fork1 and fork2
After Philosopher gets the two forks, it notify the Monitor and monitor display
the status of each Philosopher. Two consecutive Philosopher can not access the Fork
in between them at the same time. 

Code is written in Python 3  (**To run the program Python 3 is required)

To run the program
	First run the server program, which is a fork. To run the Fork Enter
		python server.py
	Then run the Monitor program, which is a monitor to display each state 
	of Philosopher. To run the Monitor Enter
		python monitor.py
	Finally, run the philosopher program. To run the philosopher Enter
		python ip_address_of_server ip_address_of_monitor
	
		(** Make sure that IP_address_of_server and ip_address_of_monitor are
		 in given order otherwise program will not work)
