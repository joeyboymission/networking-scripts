# Patching Idea

So to improve the calculator I was thinking something, since there are multiple VLAN can be created on the VLAN database, and the old script only for a single VLAN number, so think of if if there are different department for example 3 departments and have a VLAN 10, 20, and 30. so each of and have a name of department DEPT1 and DEPT2, and DEPT3 so each of them have their own separate vlan number therefore DEPT1 = VLAN 10, DEPT2 = VLAN 20, and DEPT3 - VLAN 30. when I select the full Department Detail View on each I will expect something like this as the new patches that we have made earlier

```
Department DEPT1
IP Address: 192.168.1.0/25
Subnet Mask: 255.255.255.128
VLAN Number: 10
VLAN Name: VLAN10
Number of Host: 100
Total Address: 128
Network Address: 192.168.1.0
Broadcast Address: 192.168.1.127
Range of Total IP: 192.168.1.0 - 192.168.1.127
Range of Usable IP: 192.168.1.1 - 192.168.1.126
Next Available: 192.168.1.128
Assignments:
  - Router Interface: 192.168.1.1
  - Switch: 192.168.1.2
  - End Devices: 192.168.1.3 - 192.168.1.126

Department DEPT2
IP Address: 192.168.1.128/26
Subnet Mask: 255.255.255.192
VLAN Number: 20
VLAN Name: VLAN20
Number of Host: 50
Total Address: 64
Network Address: 192.168.1.128
Broadcast Address: 192.168.1.191
Range of Total IP: 192.168.1.128 - 192.168.1.191
Range of Usable IP: 192.168.1.129 - 192.168.1.190
Next Available: 192.168.1.192
Assignments:
  - Router Interface: 192.168.1.129
  - Switch: 192.168.1.130
  - End Devices: 192.168.1.131 - 192.168.1.190

Department DEPT3
IP Address: 192.168.1.192/27
Subnet Mask: 255.255.255.224
VLAN Number: 30
VLAN Name: VLAN30
Number of Host: 25
Total Address: 32
Network Address: 192.168.1.192
Broadcast Address: 192.168.1.223
Range of Total IP: 192.168.1.192 - 192.168.1.223
Range of Usable IP: 192.168.1.193 - 192.168.1.222
Next Available: 192.168.1.224
Assignments:
  - Router Interface: 192.168.1.193
  - Switch: 192.168.1.194
  - End Devices: 192.168.1.195 - 192.168.1.222
```

on this case what if we have 3 departments therefore we have 3 vlans this is to have an intervlan connection and remote management to the other switches therefore it will be need to have a vlan for other routers and have a dedicated assigned IP like this

This state is when `enabled` show the intervlan, therefore it consumed some usable IP address as shown
```
Department DEPT1
IP Address: 192.168.1.0/25
Subnet Mask: 255.255.255.128
VLAN Number: 10
VLAN Name: VLAN10
Number of Host: 100
Total Address: 128
Network Address: 192.168.1.0
Broadcast Address: 192.168.1.127
Range of Total IP: 192.168.1.0 - 192.168.1.127
Range of Usable IP: 192.168.1.1 - 192.168.1.126
Next Available: 192.168.1.128
Assignments:
  - Router Interface: 192.168.1.1
  - Switch: 192.168.1.2
    - Inter VLAN Management
    - Switch DEPT2 (VLAN20 | 20): 192.168.1.131 255.255.255.192
    - Switch DEPT3 (VLAN30 | 30): 192.168.1.195 255.255.255.224
  - End Devices: 192.168.1.5 - 192.168.1.126

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 

Department DEPT2
IP Address: 192.168.1.128/26
Subnet Mask: 255.255.255.192
VLAN Number: 20
VLAN Name: VLAN20
Number of Host: 50
Total Address: 64
Network Address: 192.168.1.128
Broadcast Address: 192.168.1.191
Range of Total IP: 192.168.1.128 - 192.168.1.191
Range of Usable IP: 192.168.1.129 - 192.168.1.190
Next Available: 192.168.1.192
Assignments:
  - Router Interface: 192.168.1.129
  - Switch: 192.168.1.130
    - Inter VLAN Management
    - Switch DEPT1 (VLAN10 | 10): 192.168.1.3 255.255.255.128
    - Switch DEPT3 (VLAN30 | 30): 192.168.1.196 255.255.255.224
  - End Devices: 192.168.1.133 - 192.168.1.190

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 

Department DEPT3
IP Address: 192.168.1.192/27
Subnet Mask: 255.255.255.224
VLAN Number: 30
VLAN Name: VLAN30
Number of Host: 25
Total Address: 32
Network Address: 192.168.1.192
Broadcast Address: 192.168.1.223
Range of Total IP: 192.168.1.192 - 192.168.1.223
Range of Usable IP: 192.168.1.193 - 192.168.1.222
Next Available: 192.168.1.224
Assignments:
  - Router Interface: 192.168.1.193
  - Switch: 192.168.1.194
    - Inter VLAN Management
    - Switch DEPT1 (VLAN10 | 10): 192.168.1.4 255.255.255.128
    - Switch DEPT2 (VLAN20 | 20): 192.168.1.132 255.255.255.192
  - End Devices: 192.168.1.197 - 192.168.1.222

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 
```

This state is when `disabled` show the intervlan, therefore it does not consumed some usable IP address as shown
```
Department DEPT1
IP Address: 192.168.1.0/25
Subnet Mask: 255.255.255.128
VLAN Number: 10
VLAN Name: VLAN10
Number of Host: 100
Total Address: 128
Network Address: 192.168.1.0
Broadcast Address: 192.168.1.127
Range of Total IP: 192.168.1.0 - 192.168.1.127
Range of Usable IP: 192.168.1.1 - 192.168.1.126
Next Available: 192.168.1.128
Assignments:
  - Router Interface: 192.168.1.1
  - Switch: 192.168.1.2
  - End Devices: 192.168.1.3 - 192.168.1.126

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 

Department DEPT2
IP Address: 192.168.1.128/26
Subnet Mask: 255.255.255.192
VLAN Number: 20
VLAN Name: VLAN20
Number of Host: 50
Total Address: 64
Network Address: 192.168.1.128
Broadcast Address: 192.168.1.191
Range of Total IP: 192.168.1.128 - 192.168.1.191
Range of Usable IP: 192.168.1.129 - 192.168.1.190
Next Available: 192.168.1.192
Assignments:
  - Router Interface: 192.168.1.129
  - Switch: 192.168.1.130
  - End Devices: 192.168.1.131 - 192.168.1.190

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 

Department DEPT3
IP Address: 192.168.1.192/27
Subnet Mask: 255.255.255.224
VLAN Number: 30
VLAN Name: VLAN30
Number of Host: 25
Total Address: 32
Network Address: 192.168.1.192
Broadcast Address: 192.168.1.223
Range of Total IP: 192.168.1.192 - 192.168.1.223
Range of Usable IP: 192.168.1.193 - 192.168.1.222
Next Available: 192.168.1.224
Assignments:
  - Router Interface: 192.168.1.193
  - Switch: 192.168.1.194
  - End Devices: 192.168.1.195 - 192.168.1.222

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• 1. Edit Department Name
• 2. Edit VLAN
• 3. Copy to Clipboard
• 4. Show InterVLAN Management
• 5. Return to Map of IP Address Summary
➤ Select an action (1-4):
> 
```


Therefore this way, instead of remote management using from end device to ints own access vlan, we can now intervlan to the other vlan of the other switches that is why this is a useful additional feature

about the option `Show InterVLAN Mangement` it will show or hide the interVLAN threfore if show then it will consume a useable IP address if hide then back to normal state where only its own vlan switch is being used.

```
• 4. Hide InterVLAN Management
```
when enabled

```
• 4. Show InterVLAN Management
when disabled
note by default the Show/Hide InterVLAN Management is disable by default so that it is in the normal state


Okay how about in the part of `Mapping of IP Address Summary`

```
══════════════════════════════════════════════════
MAPPING OF IP ADDRESS SUMMARY
══════════════════════════════════════════════════
Address Usage: 224/256 (87.5%)

──────────────────────────────────────────────────
Departments
──────────────────────────────────────────────────
• 1. Department DEPT1 (126 usable hosts)
• 2. Department DEPT2 (62 usable hosts)
• 3. Department DEPT3 (30 usable hosts)
• 4. End the Program

```

I just want to add and improve some modifications here like putting it on an action button to make it separate

```
══════════════════════════════════════════════════
MAPPING OF IP ADDRESS SUMMARY
══════════════════════════════════════════════════
Address Usage: 224/256 (87.5%)

──────────────────────────────────────────────────
Departments
──────────────────────────────────────────────────
• 1. Department DEPT1 (126 usable hosts)
• 2. Department DEPT2 (62 usable hosts)
• 3. Department DEPT3 (30 usable hosts)

──────────────────────────────────────────────
Action
──────────────────────────────────────────────
• A. Router Gateway Address (copy to the clipboard)
• B. End the Program
➤ Select an action (A-B):
>

```
The `Router Gateway Address (copy to the clipboard)` is the whole compiled copy of all of the router gateway address, if the given example have a 3 gateway that corresponds to different vlan therefore I was expecting an output like this when copy to clipboard

note that the Select Action can handles even lowercase alphabet

```
Router Gateway
DEPT1 VLAN10: 192.168.1.1 255.255.255.128
DEPT2 VLAN20: 192.168.1.129 255.255.255.192
DEPT3 VLAN30: 192.168.1.193 255.255.255.224
```
This way so that it is easy for me of getting all of the gateway for the routing or sub-interfaces

note all of the parameters and values that is provided is for a reference and placeholder value only, do not hardcoded it therefore the code must be flexible and adaptable inb different scenarios


## More context
For to you to be aware and more context here are the samples only when I subnetting VLSM number of host and some parameters that may help you to compose the script

ERS SWITCH
IP Address: 172.50.224.0/22
Mask: 255.255.252.0
VLAN: 101

Starting IP: 172.50.224.0
Ending IP: 172.50.227.255

Usable Range: 172.50.224.1 - 172.50.227.254
Default Gateway; 172.50.224.1

Remote Management IP:
VLAN 101:

IP Mapping:
Server Address172.50.224.2

COE
IP Address: 172.50.228.0/23
Mask: 255.255.254.0
VLAN: 60

Starting IP: 172.50.228.0
Ending IP: 172.50.229.255

Usable Range: 172.50.228.1 - 172.50.229.254
Default Gateway: 172.50.228.1

Remote Management IP:
VLAN10: 172.50.232.3
VLAN20: 172.50.235.3
VLAN30: 172.50.233.3
VLAN40: 172.50.234.3
VLAN50: 172.50.230.3
VLAN60: 172.50.228.3
VLAN99: 172.50.235.130

PC1: 172.50.228.2
PC2:172.50.229.254

COS
IP Address: 172.50.230.0/23
Mask: 255.255.254.0
VLAN: 50

Starting IP: 172.50.230.0
Ending IP: 172.50.231.255

Usable Range: 172.50.230.1 - 172.50.231.254
Default Gateway; 172.50.230.1

Remote Management IP:
VLAN10: 172.50.232.4 
VLAN20: 172.50.235.4
VLAN30: 172.50.233.4
VLAN40: 172.50.234.4
VLAN50: 172.50.230.4
VLAN60: 172.50.228.4
VLAN99: 172.50.230.131

PC12: 172.50.230.2
PC14:172.50.231.254

CIT
IP Address: 172.50.232.0/24
Mask: 255.255.255.0
VLAN: 10

Starting IP: 172.50.232.0
Ending IP: 172.50.232.255

Usable Range: 172.50.232.1 - 172.50.232.254
Default Gateway: 172.50.232.1

Remote Management IP:
VLAN10: 172.50.232.5
VLAN20: 172.50.235.5
VLAN30: 172.50.233.5
VLAN40: 172.50.234.5
VLAN50: 172.50.230.5
VLAN60: 172.50.228.5
VLAN99: 172.50.230.132

PC0: 172.50.232.2
PC2: 172.50.232.254

CAFA
IP Address: 172.50.233.0/24
Mask: 255.255.255.0
VLAN: 30

Starting IP: 172.50.233.0
Ending IP: 172.50.233.255

Usable Range: 172.50.233.1 - 172.50.233.254
Default Gateway: 172.50.233.1

Remote Management IP:
VLAN10: 172.50.232.6
VLAN20: 172.50.235.6
VLAN30: 172.50.233.6
VLAN40: 172.50.234.6
VLAN50: 172.50.2306
VLAN60: 172.50.228.6
VLAN99: 172.50.230.133

PC6: 172.50.233.2
PC8: 172.50.233.254

CLA
IP Address: 172.50.234.0/24
Mask: 255.255.255.0
VLAN: 40

Starting IP: 172.50.234.0
Ending IP: 172.50.234.255

Usable Range: 172.50.234.1 - 172.50.234.254
Default Gateway: 172.50.234.1

Remote Management IP:
VLAN10: 172.50.232.7
VLAN20: 172.50.235.7
VLAN30: 172.50.233.7
VLAN40: 172.50.234.7
VLAN50: 172.50.230.7
VLAN60: 172.50.228.7
VLAN99: 172.50.230.134

PC9: 172.50.234.2
PC11: 172.50.234.254

IRTC
IP Address: 172.50.235.0/25
Mask: 255.255.255.128
VLAN: 20

Starting IP: 172.50.235.0
Ending IP: 172.50.235.126

Usable Range: 172.50.235.1 - 172.50.235.126
Default Gateway: 172.50.235.1

Remote Management IP:
VLAN10: 172.50.232.8
VLAN20: 172.50.235.8
VLAN30: 172.50.233.8
VLAN40: 172.50.234.8
VLAN50: 172.50.230.8
VLAN60: 172.50.228.8
VLAN99: 172.50.230.135

PC3: 172.50.235.2
PC5: 172.50.235.126

MGT
IP Address: 172.50.235.128/27
Mask: 255.255.255.224
VLAN: 99

Starting IP: 172.50.235.128
Ending IP: 172.50.235.159

Usable Range: 172.50.235.129 - 172.50.235.158
Default Gateway: 172.50.235.129

Remote Management IP:
VLAN10: 172.50.232..9
VLAN20: 172.50.235.9
VLAN30: 172.50.233.9
VLAN40: 172.50.234.9
VLAN50: 172.50.230.9
VLAN60: 172.50.228.9
VLAN99: 172.50.230.136

Laptop0: 172.50.235.130
Laptop1:172.50.235.158


This time focus how the `Remote Management IP` was assigned, but follow the main request instruction of change above, this is for reference only