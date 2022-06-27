Thanks for taking the time to look at my project!

I am currently working on a scanner to help automate the enumeration phase of a pen-test.

NOTE: autorecon and python-nmap already have professional code to accomplish some of the functionality I am working on. 
I am just doing this for fun and for practice.

Requirements: 

- python 3.10.x
- nmap
- xmltodict
- pandas
	
	

Below are the functions I have created so far and upcoming goals


Current functions:
- ping sweep to check for live hosts
- nmap launch on resulting hosts for all ports with verbose output, saving results to xml file 
- xml to csv for more readable output

Goals:
- dirb for all 443 and 80 ports
- xxs, sql injection, xsrf modules
- launching other nmap scripts on susceptible services
- multi-threaded processing for quicker turnaround time 
	-(threads will be implemented last but is a must! Scans take an incredible amount of time and pen-tests are typically time-crunched as is)
