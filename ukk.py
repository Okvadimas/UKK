import paramiko
import time
import getpass

hostname = str(input("Hostname : "))
username = str(input("Username : "))
password = str(input("Password : "))

if len(hostname) == 0 and len(username) == 0 and len(password) == 0:
    hostname = "[fe80::a00:27ff:fe90:c130%24]"
    username = "admin"
    password = ""

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname, username=username, password=password, allow_agent=False, look_for_keys=False)

print(f"\nSuccesfully Login as {username}")
time.sleep(2)
print("Starting Mikrotik Network Automation")
time.sleep(1)
print("*"*50)

def configureA():
    configurationA = [
        "system identity set name=Router-A",
        "interface vlan add name=TEKNIS vlan-id=10 interface=ether2 comment=Vlan10-Teknis",
        "interface vlan add name=HRD vlan-id=20 interface=ether2 comment=Vlan20-Hrd",
        "ip address add address=10.100.100.1/30 interface=ether1",
        "ip address add address=192.168.10.1/25 interface=TEKNIS",
        "ip address add address=192.168.20.1/28 interface=HRD",
        'ip dns cache flush',
        "ip dns static add name=smkbisa.id address=172.16.5.1",
        "ip dns set servers=10.100.100.2 allow-remote-requests=yes",
        "user add name=administrator password=stembajuara group=full",
        "user group add name=support policy=api,ftp,read,romon,sniff,telnet,tikapp,winbox,dude,local,reboot,sensitive,ssh,test,web,write",
        "user add name=support password=stembamantap group=support",
        "user add name=tukangbackup password=stembajiwa group=read",
        "queue simple add name=Vlan10-Teknis target=TEKNIS max-limit=5M/5M",
        "queue simple add name=Vlan20-Hrd target=HRD max-limit=1M/1M",
        "ip dhcp-server add name=Vlan10 interface=TEKNIS address-pool=dhcp_pool0 disabled=no",
        "ip route add dst-address=172.16.5.0/29 gateway=10.100.100.2"
    ]

    for config in configurationA:
        ssh_client.exec_command(config)
        time.sleep(0.5)

    print("\n")
    print("-" * 7, "Successfully Updated Configuration in Router-A", "-" * 7)
    print("*" * 50)

def configureB():
    configurationB = [
        "system identity set name=Router-B",
        "ip address add address=10.100.100.2/30 interface=ether1",
        "ip address add address=172.16.5.4/29 interface=ether2",
        'ip dns cache flush',
        "ip dns static add name=smkbisa.id address=172.16.5.1",
        "ip dns set allow-remote-requests=yes",
        "user add name=administrator password=stembajuara group=full",
        "user group add name=support policy=api,ftp,read,romon,sniff,telnet,tikapp,winbox,dude,local,reboot,sensitive,ssh,test,web,write",
        "user add name=support password=stembamantap group=support",
        "user add name=tukangbackup password=stembajiwa group=read",
        "ip route add dst-address=192.168.10.0/25 gateway=10.100.100.1",
        "ip route add dst-address=192.168.20.0/28 gateway=10.100.100.1"
    ]

    for config in configurationB:
        ssh_client.exec_command(config)
        time.sleep(0.5)

    print("\n")
    print("-" * 7, "Successfully Updated Configuration in Router-B", "-" * 7)
    print("*" * 50)

def configureSwitch():
    pass

def resetRouter():
    config = "system reset-configuration no-defaults=yes"
    ssh_client.exec_command(config)

def babi():
    quit()

def choose():
    print("""
    NB : 1. Router-A
         2. Router-B
         3. Switch
         4. Reset Router
         5. Exit
    Choose with Integer/Number
        """)
    device = int(input("Device : "))

    if device == 1:
        configureA()
    elif device == 2:
        configureB()
    elif device == 3 :
        configureSwitch()
    elif device == 4:
        resetRouter()
    elif device == 5:
        babi()
    else:
        print("Something Went Wrong")
        choose()



choose()
