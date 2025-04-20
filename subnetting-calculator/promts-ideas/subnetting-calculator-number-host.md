# Subnetting Calculator - Number of Host
Description: This is a documentation and prompt for the composition of the script named `subnetting-calculator-number-host.py`. Below you can see my customed prompt on making the script calculator.

You are free to contribute to this project by submitting an `Issue` on the Gihub or making a separate branch for this so that I can check and analyze th improvement!

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
NUMBER OF HOST SUBNETTING CALCULATOR (IPv4
-------------------------------------------
Enter the IP Address
>

Select which Subnet Mask or CIDR?
1. Subnet Mask
2. CIDR

```
Note: add an error handling when the user incorrects the input

if the user selects the `1` as `Subnet Mask` then
```
Enter the Subnet Mask (format 255.255.255.255)
>
```
Note: add an error handling when the user incorrects the input

if the user selects the `2` as `CIDR` then
```
Enter the CIDR (/n where n is the given number of bits)
>
```

if any of the options from the `Select which Subnet Mask or CIDR?` then proceed to this:
```
How many area/departments/partition does required
>
```
Note: The user must input a whole real numbers as corresponds to how many number of area/departments/buildings. If the user succesfully type then:

```
Please name the Department (1 of N)

```
Note: The user must put the custom naming for the department, then the N is how many department that user defined in the previous. The number of departments corresponds on how many user defined on the previous so be aware of that. The naming will end up until all of the numbered departments were met. If done then here is the next:

```
How many host on Department [custom name]
>
```

Now the user must iput a whole real number number of host as required on the prompt. So host are the devices that are be provided usable IP address. The [custom name] is the user defined custom named based on the previous prompt so be aware of that.

if the user satisfies the condition then next will be this:
```
-------------------------------------------
MAPPING OF IP ADDRESS
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
```
Department [Custom Name]
Number of Host:
Total Address (Including Network and Broadcast): 

```