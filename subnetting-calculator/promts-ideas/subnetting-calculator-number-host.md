# Subnetting Calculator - Number of Host
Description: This is a documentation and prompt for the composition of the script named `subnetting-calculator-number-host.py`. Below you can see my customed prompt on making the script calculator.

You are free to contribute to this project by submitting an `Issue` on the Gihub or making a separate branch for this so that I can check and analyze th improvement!

Note:
The `Prompt` is an instruction/command used to composed and create the script.

## Tools and Resources
Here are the tools and resources that I have used to composed this calculator:
- Visual Studio Code
- Grok (Grok 3)
- Github Copilot
- Python

## Promt
on this chat session that has a titled `subnetting-calculator-number-host` in which I provided a sample context that is from the preliminary examination, I allow you first to observe the given problem then here is the command.

Based on the exam as you can observe that this given problem provides the IP address, the Subnet Mask/CIDR and the number of host per department. What if I create a script calculator that provides me the answer:
- how many subnet can create based of how many area/departments/buildings
- what are the network ID and the broadcast ID of each subnets
- what are the total possible IP address per subnet
- what are the total usable IP address per subnet

Also the calculator will ask some information like:
- what is the given IP address
- does the problem used Subnet Mask/CIDR
- if Subnet Mask then, the user must type the subnet value (255.255.255.255 example format), else the user must provide the CIDR value (/n where the n is the number of the given CIDR)


GUI OF THE CLI
The user must run the script named `subnetting-calculator-number-host` using the cli `python subnetting-calculator-number-host` once run here is the GUI, note that every steps in GUI have their correspond tagging system so that when I infer on what GUI that I referring to you can jump and look for it e.g. GUI A., GUI B1, GUI A2 and many more:

GUI A.:
```
-------------------------------------------
NUMBER OF HOST SUBNETTING CALCULATOR (IPv4)
-------------------------------------------
Enter the IP Address
>

Select which Subnet Mask or CIDR?
1. Subnet Mask
2. CIDR

```
Note: add an error handling when the user incorrects the input

if the user selects the `1` as `Subnet Mask` then

GUI B1.:
```
Enter the Subnet Mask (format 255.255.255.255)
>
```
Note: add an error handling when the user incorrects the input

if the user selects the `2` as `CIDR` then

GUI B2.:
```
Enter the CIDR:
>
```
Note: On this the user can input a whole integer number ranging from 8 to 32, even without the `/` slash the program still accepts the input.

if any of the options from the `Select which Subnet Mask or CIDR?` then proceed to this:

GUI C:
```
How many area/departments/partition does required
>
```
Note: The user must input a whole real numbers as corresponds to how many number of area/departments/buildings. If the user succesfully type then:

GUI D.:
```
Please name the Department (1 of N)

```
Note: The user must put the custom naming for the department, then the N is how many department that user defined in the previous. The number of departments corresponds on how many user defined on the previous so be aware of that. The naming will end up until all of the numbered departments were met. If done then here is the next:

GUI E.:
```
How many host on Department [custom name]
>
```

Now the user must iput a whole real number number of host as required on the prompt. So host are the devices that are be provided usable IP address. The [custom name] is the user defined custom named based on the previous prompt so be aware of that.

if the user satisfies the condition then next will be this:

GUI F.:
```
Does every department/buildings have their own VLAN?
1. Yes
2. No
>
```
Note: the user must select if the certain department/building have their own VLAN, if the user selects `1` meaning `Yes` then the GUI:

GUI G1.:
```
Input VLAN number for Department [custom name]
Number: >
```
after succesfully input the VLAN number subsequently go to its name before going to another department

GUI G1.1
```
Name: >
```
Then this procedure finished up untill all of the department is finished

Note: First the user must put the number of the VLAN number, the default `1` cannot be input so if the user put that the program will reject and try again. The user input must input a whole real number. For the name any of the string can input

if the user selects the option `2` in the GUI F then proceed to this, dont worry the user can customize and edit every department to add or edit in every department. The next GUI will proceed to this

GUI H.
```
-------------------------------------------
MAPPING OF IP ADDRESS SUMMARY
-------------------------------------------
1. Department [custom name]
2. Department [custom name]
.
.
.
Please select which departments/building:
>

```
Note: I cant defined all of the Department but above is the only example, the number of department changes dynamically based on the previous assigned number and customed named by the user. The options are numbered so the user must select the option number otherwise there is a error handling to try again choose. Put the `End the Program` option at the end of the list of the options I cant defined now because this will be dynamically changes based on how many Department defined by the user.

if the user for example select any of the option here is the next:

GUI I.
```
Department [Custom Name]
IP Address:
VLAN Number:
VLAN Name:
Number of Host:
Total Address (Including Network and Broadcast): 
Range of Usable IP: 
Next Available: 
Assignments:
- Router Interface
- Switch
- End Devices [ x.x.x.x - x.x.x.x this is the range for the end devices]

Action:
1. Edit Department Name:
2. Edit VLAN:
3. Return to Map of IP Address Summary

```

Note: 
- On the detailed GUI from the `GUI I` you can see several lines such as the:
  - Department - this is the user defined custom name and can be edit on the `Action` option, when selected it will look like from the `GUI D.` but this time this is the specific department will be edited only.
  - IP Address: This will be composed of 4 octets along with its slash notation CIDR at the end example `192.168.1.1/24`. This defines the representation IP of the whole IP.
  - Number of Host - this was the given number of host defined by the user as shown in the `GUI E.`.
  - Total Address - is the number of total address including the network and broadcast IP. In which `Host Number + (Network + Broadcast Address)`.
  - Range of Usable IP - it is the range from the first usable IP address up to The last.
  - Assignemnts - These are the part where the assign of IP address
    - Router Interface - first usable IP address, this is used for ping or remote management address of the router or the gateway IP address
    - Switch - 2nd usable IP address, this is used for ping or remote management address usually assigned for the VLAN (like defaut vlan 1).
    - End devices - Is the usable IP address assigned to the end devices usually this is defined as the number of host as indicated in the `GUI E.`



Overall Note:
Some of the procedure and steps from the GUI might be a sample test or I am thinking of way to approach them but nonetheless this is what I have thinking for the outline. To you to have a full context you can rely on the sample context below, note that do not rely on that sample might be different if another sample has been inputted here.

## Context
Checkout for Script Calculator

Problem Statement
A network administrator is tasked with designing a network addressing scheme for the TUP-Manila campus network connection with the following details:

IP Address: 172.30.240.0/22  
Subnet Mask: 255.255.252.0

Instructions

Design an addressing scheme for the following network requirements:TUP-Manila Number of Host Addresses (Usable Hosts for Internet Access Computers):  

CAFA: 24 hosts  
CIE: 25 hosts  
CIT: 63 hosts  
COS: 30 hosts  
COE: 30 hosts  
CLA: 20 hosts  
ADMIN: 300 hosts

Total Addresses (Including Network and Broadcast):  

CAFA: 24 + 2 = 26 total addresses  
CIE: 25 + 2 = 27 total addresses  
CIT: 63 + 2 = 65 total addresses  
COS: 30 + 2 = 32 total addresses  
COE: 30 + 2 = 32 total addresses  
CLA: 20 + 2 = 22 total addresses  
ADMIN: 300 + 2 = 302 total addresses


Design the network topology and map the addresses to connect the network devices, using only the first and last usable addresses of a subnet for PCs.  

Calculate the IP addressing scheme and provide detailed computations (total addresses, usable addresses, network address, broadcast address, and usable range).  

Secure the devices physically and at the network level.  

Configure the network for internet connectivity.


Devices

1 Router: Router-PT-Empty (TUP-MANILA)  
1 Cloud: Cloud-PT (INTERNET)  
7 Switches: 2960-24TT (CAFA, CIE, CIT, COS, COE, CLA, ADMIN)  
1 Multilayer Switch: 356024PS (MAIN-SWITCH)

VLAN Assignments

CAFA: VLAN 50 (VLAN50)  
CIE: VLAN 60 (VLAN60)  
CIT: VLAN 20 (VLAN20)  
COS: VLAN 30 (VLAN30)  
COE: VLAN 40 (VLAN40)  
CLA: VLAN 70 (VLAN70)  
ADMIN: VLAN 10 (VLAN10)


Expectations for the AI
The AI should:  

Use a Router-on-a-Stick configuration where the router (TUP-MANILA) handles inter-VLAN routing via a single trunk link to the MAIN-SWITCH.  
Assign management IPs to all switches:  
Use the second usable address in each department’s subnet for the departmental switch (e.g., CAFA switch gets the second usable address in CAFA’s subnet).  
MAIN-SWITCH management IP should be in the ADMIN subnet, using the third usable address (172.30.240.3).


Configure VLANs for each department as specified above, with appropriate access and trunk ports:  
Access ports for PCs on departmental switches (e.g., CAFA PCs in VLAN 50).  
Trunk ports between switches (e.g., MAIN-SWITCH to CAFA switch carrying VLAN 50).


Provide detailed subnet calculations for each department, including:  
Total possible addresses (2^n)  
Usable addresses (total - 2)  
Network address  
Broadcast address  
Range of usable addresses


Map addresses as follows:  
First usable address: Router sub-interface (default gateway)  
Second usable address: Departmental switch management IP  
Third usable address: First PC  
Last usable address: Second PC


Include CLI commands for all devices (router, switches, and PCs) in Cisco Packet Tracer format, reflecting the latest IP ranges and configurations.  
Implement security measures (physical and network) as specified.  
Ensure internet connectivity with NAT, a default route, and DNS configuration.  
Archive all updates in the session database for future reference.  
If modifications are requested, provide updated CLI commands and maintain consistency with the existing setup (e.g., VLANs, Router-on-a-Stick).


Latest Network Design Details
Step 1: Addressing Scheme
Base Network: 172.30.240.0/22  

Subnet Mask: 255.255.252.0 (/22)  
Total Addresses: 2^(32-22) = 2^10 = 1024  
Usable Addresses: 1024 - 2 = 1022

Subnet Calculations:Subnets are allocated based on total addresses (usable hosts + network + broadcast), sorted by size (largest to smallest):

ADMIN: 302 total addresses → /23 (2^9 = 512 addresses)  

Usable: 512 - 2 = 510  
Subnet: 172.30.240.0/23  
Network Address: 172.30.240.0  
Broadcast Address: 172.30.241.255  
Range: 172.30.240.0 to 172.30.241.255  
Usable Range: 172.30.240.1 to 172.30.241.254  
Next Available: 172.30.242.0


CIT: 65 total addresses → /25 (2^7 = 128 addresses)  

Usable: 128 - 2 = 126  
Subnet: 172.30.242.0/25  
Network Address: 172.30.242.0  
Broadcast Address: 172.30.242.127  
Range: 172.30.242.0 to 172.30.242.127  
Usable Range: 172.30.242.1 to 172.30.242.126  
Next Available: 172.30.242.128


COS: 32 total addresses → /26 (2^6 = 64 addresses)  

Usable: 64 - 2 = 62  
Subnet: 172.30.242.128/26  
Network Address: 172.30.242.128  
Broadcast Address: 172.30.242.191  
Range: 172.30.242.128 to 172.30.242.191  
Usable Range: 172.30.242.129 to 172.30.242.190  
Next Available: 172.30.242.192


COE: 32 total addresses → /26 (2^6 = 64 addresses)  

Usable: 64 - 2 = 62  
Subnet: 172.30.242.192/26  
Network Address: 172.30.242.192  
Broadcast Address: 172.30.242.255  
Range: 172.30.242.192 to 172.30.242.255  
Usable Range: 172.30.242.193 to 172.30.242.254  
Next Available: 172.30.243.0


CAFA: 26 total addresses → /27 (2^5 = 32 addresses)  

Usable: 32 - 2 = 30  
Subnet: 172.30.243.0/27  
Network Address: 172.30.243.0  
Broadcast Address: 172.30.243.31  
Range: 172.30.243.0 to 172.30.243.31  
Usable Range: 172.30.243.1 to 172.30.243.30  
Next Available: 172.30.243.32


CIE: 27 total addresses → /27 (2^5 = 32 addresses)  

Usable: 32 - 2 = 30  
Subnet: 172.30.243.32/27  
Network Address: 172.30.243.32  
Broadcast Address: 172.30.243.63  
Range: 172.30.243.32 to 172.30.243.63  
Usable Range: 172.30.243.33 to 172.30.243.62  
Next Available: 172.30.243.64


CLA: 22 total addresses → /27 (2^5 = 32 addresses)  

Usable: 32 - 2 = 30  
Subnet: 172.30.243.64/27  
Network Address: 172.30.243.64  
Broadcast Address: 172.30.243.95  
Range: 172.30.243.64 to 172.30.243.95  
Usable Range: 172.30.243.65 to 172.30.243.94  
Next Available: 172.30.243.96



Total Address Usage: 512 (ADMIN) + 128 (CIT) + 64 (COS) + 64 (COE) + 32 (CAFA) + 32 (CIE) + 32 (CLA) = 864 addresses (fits within 1024).
Step 2: Network Topology and Address Mapping
Topology (Router-on-a-Stick):  

INTERNET (Cloud-PT)  
Eth6 to TUP-MANILA Gig 1/0


TUP-MANILA (Router-PT-Empty)  
Gig 0/0 to MAIN-SWITCH Gig 0/1 (Trunk, VLANs 10,20,30,40,50,60,70)  
Gig 1/0 to INTERNET Eth6


MAIN-SWITCH (356024PS)  
Gig 0/1 to TUP-MANILA Gig 0/0 (Trunk, VLANs 10,20,30,40,50,60,70)  
Fa 0/1 to CAFA Gig 0/1 (Trunk, VLAN 50)  
Fa 0/2 to CIE Gig 0/1 (Trunk, VLAN 60)  
Fa 0/3 to ADMIN Gig 0/1 (Trunk, VLAN 10)  
Fa 0/4 to CIT Gig 0/1 (Trunk, VLAN 20)  
Fa 0/5 to COS Gig 0/1 (Trunk, VLAN 30)  
Fa 0/6 to COE Gig 0/1 (Trunk, VLAN 40)  
Fa 0/7 to CLA Gig 0/1 (Trunk, VLAN 70)


CAFA (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/1 (Trunk, VLAN 50)  
Fa 0/1 to PC0 Fa0 (Access, VLAN 50)  
Fa 0/2 to PC1 Fa0 (Access, VLAN 50)


CIE (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/2 (Trunk, VLAN 60)  
Fa 0/1 to PC2 Fa0 (Access, VLAN 60)  
Fa 0/2 to PC3 Fa0 (Access, VLAN 60)


ADMIN (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/3 (Trunk, VLAN 10)  
Fa 0/1 to PC4 Fa0 (Access, VLAN 10)  
Fa 0/2 to PC5 Fa0 (Access, VLAN 10)


CIT (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/4 (Trunk, VLAN 20)  
Fa 0/1 to PC6 Fa0 (Access, VLAN 20)  
Fa 0/2 to PC7 Fa0 (Access, VLAN 20)


COS (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/5 (Trunk, VLAN 30)  
Fa 0/1 to PC8 Fa0 (Access, VLAN 30)  
Fa 0/2 to PC9 Fa0 (Access, VLAN 30)


COE (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/6 (Trunk, VLAN 40)  
Fa 0/1 to PC10 Fa0 (Access, VLAN 40)  
Fa 0/2 to PC11 Fa0 (Access, VLAN 40)


CLA (2960-24TT)  
Gig 0/1 to MAIN-SWITCH Fa 0/7 (Trunk, VLAN 70)  
Fa 0/1 to PC12 Fa0 (Access, VLAN 70)  
Fa 0/2 to PC13 Fa0 (Access, VLAN 70)



Address Mapping:  

ADMIN (172.30.240.0/23, VLAN 10):  
Router Sub-Interface (Gig0/0.10): 172.30.240.1  
Switch (ADMIN): 172.30.240.2  
MAIN-SWITCH: 172.30.240.3  
PC4: 172.30.240.4  
PC5: 172.30.241.254


CIT (172.30.242.0/25, VLAN 20):  
Router Sub-Interface (Gig0/0.20): 172.30.242.1  
Switch (CIT): 172.30.242.2  
PC6: 172.30.242.3  
PC7: 172.30.242.126


COS (172.30.242.128/26, VLAN 30):  
Router Sub-Interface (Gig0/0.30): 172.30.242.129  
Switch (COS): 172.30.242.130  
PC8: 172.30.242.131  
PC9: 172.30.242.190


COE (172.30.242.192/26, VLAN 40):  
Router Sub-Interface (Gig0/0.40): 172.30.242.193  
Switch (COE): 172.30.242.194  
PC10: 172.30.242.195  
PC11: 172.30.242.254


CAFA (172.30.243.0/27, VLAN 50):  
Router Sub-Interface (Gig0/0.50): 172.30.243.1  
Switch (CAFA): 172.30.243.2  
PC0: 172.30.243.3  
PC1: 172.30.243.30


CIE (172.30.243.32/27, VLAN 60):  
Router Sub-Interface (Gig0/0.60): 172.30.243.33  
Switch (CIE): 172.30.243.34  
PC2: 172.30.243.35  
PC3: 172.30.243.62


CLA (172.30.243.64/27, VLAN 70):  
Router Sub-Interface (Gig0/0.70): 172.30.243.65  
Switch (CLA): 172.30.243.66  
PC12: 172.30.243.67  
PC13: 172.30.243.94



Step 3: Security Measures

Physical Security:  
Place routers, switches, and servers in locked rooms with restricted access.  
Use security cameras and access logs to monitor entry.  
Label cables and devices to prevent tampering.


Network Security:  
VLANs for each department to segregate traffic.  
Access Control Lists (ACLs) on the router to restrict inter-VLAN access.  
Strong passwords and SSH for remote access (disable Telnet).  
Disable unused switch ports.  
Enable MAC address filtering.



Step 4: Internet Connectivity

Router Configuration:  
External interface (Gig 1/0) gets a public IP (assumed via DHCP from ISP).  
NAT to map 172.30.240.0/22 to the public IP.  
Default route to ISP gateway (assumed as 203.0.113.1).


DNS: Use Google DNS (8.8.8.8).  
Firewall: Allow outbound traffic, block unsolicited inbound traffic.

Step 5: CLI Commands
TUP-MANILA (Router-PT-Empty)  
enable
configure terminal
hostname TUP-MANILA

! Configure sub-interfaces for each VLAN
interface GigabitEthernet0/0
 no ip address
 no shutdown
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 172.30.240.1 255.255.254.0
 no shutdown
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 172.30.242.1 255.255.255.128
 no shutdown
interface GigabitEthernet0/0.30
 encapsulation dot1Q 30
 ip address 172.30.242.129 255.255.255.192
 no shutdown
interface GigabitEthernet0/0.40
 encapsulation dot1Q 40
 ip address 172.30.242.193 255.255.255.192
 no shutdown
interface GigabitEthernet0/0.50
 encapsulation dot1Q 50
 ip address 172.30.243.1 255.255.255.224
 no shutdown
interface GigabitEthernet0/0.60
 encapsulation dot1Q 60
 ip address 172.30.243.33 255.255.255.224
 no shutdown
interface GigabitEthernet0/0.70
 encapsulation dot1Q 70
 ip address 172.30.243.65 255.255.255.224
 no shutdown

! Configure external interface (assume ISP provides IP)
interface GigabitEthernet1/0
 ip address dhcp
 no shutdown

! Configure NAT
ip nat inside source list 1 interface GigabitEthernet1/0 overload
access-list 1 permit 172.30.240.0 0.0.3.255
interface GigabitEthernet0/0.10
 ip nat inside
interface GigabitEthernet0/0.20
 ip nat inside
interface GigabitEthernet0/0.30
 ip nat inside
interface GigabitEthernet0/0.40
 ip nat inside
interface GigabitEthernet0/0.50
 ip nat inside
interface GigabitEthernet0/0.60
 ip nat inside
interface GigabitEthernet0/0.70
 ip nat inside
interface GigabitEthernet1/0
 ip nat outside

! Configure default route (assume ISP gateway is 203.0.113.1)
ip route 0.0.0.0 0.0.0.0 203.0.113.1

! Configure DNS
ip domain-lookup
ip name-server 8.8.8.8

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

MAIN-SWITCH (356024PS)  
enable
configure terminal
hostname MAIN-SWITCH

! Create VLANs
vlan 10
 name VLAN10
vlan 20
 name VLAN20
vlan 30
 name VLAN30
vlan 40
 name VLAN40
vlan 50
 name VLAN50
vlan 60
 name VLAN60
vlan 70
 name VLAN70

! Configure management IP in VLAN 1 (using ADMIN subnet)
interface vlan 1
 ip address 172.30.240.3 255.255.254.0
 no shutdown

! Configure default gateway (point to router's ADMIN sub-interface)
ip default-gateway 172.30.240.1

! Configure trunk port to TUP-MANILA
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,60,70

! Configure trunk ports to departmental switches
interface FastEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 50
interface FastEthernet0/2
 switchport mode trunk
 switchport trunk allowed vlan 60
interface FastEthernet0/3
 switchport mode trunk
 switchport trunk allowed vlan 10
interface FastEthernet0/4
 switchport mode trunk
 switchport trunk allowed vlan 20
interface FastEthernet0/5
 switchport mode trunk
 switchport trunk allowed vlan 30
interface FastEthernet0/6
 switchport mode trunk
 switchport trunk allowed vlan 40
interface FastEthernet0/7
 switchport mode trunk
 switchport trunk allowed vlan 70

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

CAFA Switch (2960-24TT)  
enable
configure terminal
hostname CAFA-SWITCH

! Create VLAN
vlan 50
 name VLAN50

! Configure management IP in VLAN 50
interface vlan 50
 ip address 172.30.243.2 255.255.255.224
 ip default-gateway 172.30.243.1
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 50

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 50
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 50

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

CIE Switch (2960-24TT)  
enable
configure terminal
hostname CIE-SWITCH

! Create VLAN
vlan 60
 name VLAN60

! Configure management IP in VLAN 60
interface vlan 60
 ip address 172.30.243.34 255.255.255.224
 ip default-gateway 172.30.243.33
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 60

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 60
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 60

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

ADMIN Switch (2960-24TT)  
enable
configure terminal
hostname ADMIN-SWITCH

! Create VLAN
vlan 10
 name VLAN10

! Configure management IP in VLAN 10
interface vlan 10
 ip address 172.30.240.2 255.255.254.0
 ip default-gateway 172.30.240.1
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 10

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

CIT Switch (2960-24TT)  
enable
configure terminal
hostname CIT-SWITCH

! Create VLAN
vlan 20
 name VLAN20

! Configure management IP in VLAN 20
interface vlan 20
 ip address 172.30.242.2 255.255.255.128
 ip default-gateway 172.30.242.1
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 20

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 20
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

COS Switch (2960-24TT)  
enable
configure terminal
hostname COS-SWITCH

! Create VLAN
vlan 30
 name VLAN30

! Configure management IP in VLAN 30
interface vlan 30
 ip address 172.30.242.130 255.255.255.192
 ip default-gateway 172.30.242.129
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 30

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 30
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 30

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

COE Switch (2960-24TT)  
enable
configure terminal
hostname COE-SWITCH

! Create VLAN
vlan 40
 name VLAN40

! Configure management IP in VLAN 40
interface vlan 40
 ip address 172.30.242.194 255.255.255.192
 ip default-gateway 172.30.242.193
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 40

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 40
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 40

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

CLA Switch (2960-24TT)  
enable
configure terminal
hostname CLA-SWITCH

! Create VLAN
vlan 70
 name VLAN70

! Configure management IP in VLAN 70
interface vlan 70
 ip address 172.30.243.66 255.255.255.224
 ip default-gateway 172.30.243.65
 no shutdown

! Configure trunk port to MAIN-SWITCH
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 70

! Configure access ports for PCs
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 70
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 70

! Enable SSH
ip domain-name tupmanila.local
crypto key generate rsa
 1024
username cisco password cisco
line vty 0 4
 login local
 transport input ssh
exit

PC Configurations (Static IPs)  

PC0 (CAFA, VLAN 50): IP 172.30.243.3, Subnet Mask 255.255.255.224, Gateway 172.30.243.1  
PC1 (CAFA, VLAN 50): IP 172.30.243.30, Subnet Mask 255.255.255.224, Gateway 172.30.243.1  
PC2 (CIE, VLAN 60): IP 172.30.243.35, Subnet Mask 255.255.255.224, Gateway 172.30.243.33  
PC3 (CIE, VLAN 60): IP 172.30.243.62, Subnet Mask 255.255.255.224, Gateway 172.30.243.33  
PC4 (ADMIN, VLAN 10): IP 172.30.240.4, Subnet Mask 255.255.254.0, Gateway 172.30.240.1  
PC5 (ADMIN, VLAN 10): IP 172.30.241.254, Subnet Mask 255.255.254.0, Gateway 172.30.240.1  
PC6 (CIT, VLAN 20): IP 172.30.242.3, Subnet Mask 255.255.255.128, Gateway 172.30.242.1  
PC7 (CIT, VLAN 20): IP 172.30.242.126, Subnet Mask 255.255.255.128, Gateway 172.30.242.1  
PC8 (COS, VLAN 30): IP 172.30.242.131, Subnet Mask 255.255.255.192, Gateway 172.30.242.129  
PC9 (COS, VLAN 30): IP 172.30.242.190, Subnet Mask 255.255.255.192, Gateway 172.30.242.129  
PC10 (COE, VLAN 40): IP 172.30.242.195, Subnet Mask 255.255.255.192, Gateway 172.30.242.193  
PC11 (COE, VLAN 40): IP 172.30.242.254, Subnet Mask 255.255.255.192, Gateway 172.30.242.193  
PC12 (CLA, VLAN 70): IP 172.30.243.67, Subnet Mask 255.255.255.224, Gateway 172.30.243.65  
PC13 (CLA, VLAN 70): IP 172.30.243.94, Subnet Mask 255.255.255.224, Gateway 172.30.243.65
