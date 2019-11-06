from netmiko import ConnectHandler
import sys

with open('Network_Switch_IP_Address.list')as L:
	IP_List = L.readlines()
L.close()
UserName = sys.argv[1]
UserName= str(UserName)
Password = sys.argv[2]
Password = str(Password)

content= [x.strip('\n') for x in IP_List]

for x in content:

	device_data = {
        	'device_type': 'hp_procurve',
            	'ip': x,
           	'username': UserName,
           	'password': Password,
        }




	device = ConnectHandler(**device_data)
	output = device.send_command("show running-config")

	f = open(x+'_running_config.txt','w')
	f.write (output)
	f.close()
	print x +'s running config save is completed.'
	device.disconnect()
print 'completed'
