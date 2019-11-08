from netmiko import ConnectHandler
import threading
from multiprocessing import Queue
import getpass
import sys

with open('Network_Switch_IP_Address.list')as L:
	IP_List = L.readlines()
    
L.close()
Username = input("Username: ")
password = getpass.getpass()
content= [x.strip('\n') for x in IP_List]

def ssh_session(x, output_q):
    x = x.strip('\n')
    try:
        device_data = {
            'device_type': 'hp_procurve',
            'ip': x,
            'username': Username,
            'password': password,
            }

        device = ConnectHandler(**device_data)
        output = device.send_command("show running-config")

        f = open(x+'_running_config.txt','w')
        f.write (output)
        f.close()
        print (x +'s running config save is completed.')
        device.disconnect()
    except:
        print('device '+x+ " is not reachable.")

if __name__ == "__main__":
    
    output_q = Queue()
    
    for x in IP_List:
          my_thread = threading.Thread(target=ssh_session, args=(x, output_q))
          my_thread.start()

    # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    # Retrieve everything off the queue - k is the router IP, v is output
    # You could also write this to a file, or create a file for each router
    
    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            print (k)
            print (val)
