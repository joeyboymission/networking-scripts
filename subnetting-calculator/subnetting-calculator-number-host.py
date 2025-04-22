import ipaddress
import math
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid IP address format. Please use format like 192.168.1.0")
        return False

def validate_subnet_mask(mask_str):
    try:
        parts = mask_str.split('.')
        if len(parts) != 4:
            return False
        valid_masks = [0, 128, 192, 224, 240, 248, 252, 254, 255]
        binary = ''
        for part in parts:
            part_int = int(part)
            if part_int not in valid_masks:
                return False
            binary += format(part_int, '08b')
        if '01' in binary:
            return False
        return True
    except:
        return False

def mask_to_cidr(mask):
    try:
        mask_parts = mask.split('.')
        binary = ''.join(format(int(x), '08b') for x in mask_parts)
        return sum(1 for bit in binary if bit == '1')
    except:
        return None

def calculate_subnet_details(base_ip, cidr, departments):
    try:
        parent_network = ipaddress.ip_network(f"{base_ip}/{cidr}", strict=False)
        results = []
        
        # Sort departments by number of hosts (largest first)
        sorted_depts = sorted(departments.items(), key=lambda x: x[1]['hosts'], reverse=True)
        current_address = parent_network.network_address
        
        for dept_name, dept_info in sorted_depts:
            # Calculate required subnet size
            hosts_needed = dept_info['hosts'] + 2  # Including network and broadcast
            subnet_bits = math.ceil(math.log2(hosts_needed))
            subnet_cidr = 32 - subnet_bits
            subnet_size = 2 ** subnet_bits
            
            # Check if enough address space remains
            if int(current_address) + subnet_size > int(parent_network.broadcast_address) + 1:
                print(f"{Fore.RED + Style.BRIGHT}✖ Not enough address space for {dept_name}")
                return None
            
            # Create subnet
            subnet = ipaddress.ip_network(f"{current_address}/{subnet_cidr}", strict=False)
            
            # Store department details
            dept_details = {
                'department': dept_name,
                'vlan_number': dept_info.get('vlan_number', None),
                'vlan_name': dept_info.get('vlan_name', None),
                'network_id': str(subnet.network_address),
                'broadcast': str(subnet.broadcast_address),
                'total_addresses': subnet_size,
                'usable_addresses': subnet_size - 2,
                'usable_range': f"{subnet[1]} - {subnet[-2]}" if subnet_size > 2 else "N/A",
                'router_ip': str(subnet[1]) if subnet_size > 2 else "N/A",
                'switch_ip': str(subnet[2]) if subnet_size > 3 else "N/A",
                'end_devices_range': f"{subnet[3]} - {subnet[-2]}" if subnet_size > 4 else "N/A",
                'next_available': str(subnet.broadcast_address + 1),
                'subnet_cidr': subnet_cidr  # Store specific subnet CIDR
            }
            
            results.append(dept_details)
            
            # Move to next network
            current_address = subnet.broadcast_address + 1
        
        return results
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}✖ Error in subnet calculation: {e}")
        return None

def main():
    departments = {}
    
    # GUI A
    print(f"\n{Fore.CYAN + Style.BRIGHT}{'═'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}NUMBER OF HOST SUBNETTING CALCULATOR (IPv4)")
    print(f"{Fore.CYAN + Style.BRIGHT}{'═'*50}")
    print(f"{Fore.BLUE + Style.BRIGHT}➤ Enter the IP Address:")
    while True:
        ip_input = input(f"{Fore.BLUE}> ").strip()
        if validate_ip(ip_input):
            base_ip = ip_input
            break
    
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Select Subnet Mask or CIDR")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.WHITE}• 1. Subnet Mask")
    print(f"{Fore.WHITE}• 2. CIDR")
    while True:
        choice = input(f"{Fore.BLUE + Style.BRIGHT}➤ Enter your choice (1-2):\n{Fore.BLUE}> ").strip()
        
        if choice == '1':
            # GUI B1
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}Subnet Mask Input")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            while True:
                subnet_mask = input(f"{Fore.BLUE + Style.BRIGHT}➤ Enter the Subnet Mask (format 255.255.255.255):\n{Fore.BLUE}> ").strip()
                if validate_subnet_mask(subnet_mask):
                    cidr = mask_to_cidr(subnet_mask)
                    if cidr is not None:
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid subnet mask")
                else:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Invalid subnet mask format")
            break
        elif choice == '2':
            # GUI B2
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}CIDR Input")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            while True:
                cidr_input = input(f"{Fore.BLUE + Style.BRIGHT}➤ Enter the CIDR (8-32):\n{Fore.BLUE}> ").strip()
                cidr_input = cidr_input.lstrip('/')
                try:
                    cidr = int(cidr_input)
                    if 8 <= cidr <= 32:
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}✖ CIDR must be between 8 and 32")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Invalid CIDR format")
            break
        else:
            print(f"{Fore.RED + Style.BRIGHT}✖ Please select 1 or 2")
    
    # GUI C
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Number of Departments")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    while True:
        try:
            num_depts = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ How many area/departments/partition does required:\n{Fore.BLUE}> ").strip())
            if num_depts > 0:
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Number must be positive")
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
    
    # GUI D
    dept_names = []
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Department Naming")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    for i in range(num_depts):
        while True:
            dept_name = input(f"{Fore.BLUE + Style.BRIGHT}➤ Please name the Department ({i+1} of {num_depts}):\n{Fore.BLUE}> ").strip()
            if dept_name and dept_name not in dept_names:
                dept_names.append(dept_name)
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Department name must be unique and non-empty")
    
    # GUI E
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Number of Hosts per Department")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    for dept_name in dept_names:
        while True:
            try:
                hosts = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ How many host on Department {dept_name}:\n{Fore.BLUE}> ").strip())
                if hosts > 0:
                    departments[dept_name] = {'hosts': hosts}
                    break
                print(f"{Fore.RED + Style.BRIGHT}✖ Number of hosts must be positive")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
    
    # GUI F
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}VLAN Configuration")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.WHITE}• 1. Yes")
    print(f"{Fore.WHITE}• 2. No")
    while True:
        vlan_choice = input(f"{Fore.BLUE + Style.BRIGHT}➤ Does every department/buildings have their own VLAN? (1-2):\n{Fore.BLUE}> ").strip()
        if vlan_choice in ['1', '2']:
            break
        print(f"{Fore.RED + Style.BRIGHT}✖ Please select 1 or 2")
    
    if vlan_choice == '1':
        # GUI G1 & G1.1
        print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        print(f"{Fore.CYAN + Style.BRIGHT}VLAN Number and Name Assignment")
        print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        for dept_name in dept_names:
            while True:
                try:
                    vlan_num = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ Input VLAN number for Department {dept_name}:\n{Fore.BLUE}Number: > ").strip())
                    if vlan_num != 1 and vlan_num > 0:
                        break
                    print(f"{Fore.RED + Style.BRIGHT}✖ VLAN number cannot be 1 and must be positive")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
            
            vlan_name = input(f"{Fore.BLUE + Style.BRIGHT}Name: > ").strip()
            if not vlan_name:
                vlan_name = f"VLAN{vlan_num}"
            departments[dept_name]['vlan_number'] = vlan_num
            departments[dept_name]['vlan_name'] = vlan_name
    
    # Calculate subnet details
    subnet_details = calculate_subnet_details(base_ip, cidr, departments)
    if not subnet_details:
        print(f"{Fore.RED + Style.BRIGHT}✖ Failed to calculate subnets. Exiting.")
        return
    
    while True:
        # GUI H
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{Fore.CYAN + Style.BRIGHT}{'═'*50}")
        print(f"{Fore.CYAN + Style.BRIGHT}MAPPING OF IP ADDRESS SUMMARY")
        print(f"{Fore.CYAN + Style.BRIGHT}{'═'*50}")
        total_used = sum(detail['total_addresses'] for detail in subnet_details)
        parent_addresses = 2 ** (32 - cidr)
        print(f"{Fore.WHITE}Address Usage: {Fore.GREEN}{total_used}/{parent_addresses} ({total_used/parent_addresses*100:.1f}%)")
        print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        print(f"{Fore.CYAN + Style.BRIGHT}Departments")
        print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        for i, detail in enumerate(subnet_details, 1):
            print(f"{Fore.WHITE}• {i}. Department {Fore.GREEN}{detail['department']}")
        print(f"{Fore.WHITE}• {len(subnet_details) + 1}. End the Program")
        
        try:
            choice = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ Please select which departments/building:\n{Fore.BLUE}> ").strip())
            if choice == len(subnet_details) + 1:
                print(f"\n{Fore.CYAN + Style.BRIGHT}✔ Program ended.")
                break
            if 1 <= choice <= len(subnet_details):
                selected_dept = subnet_details[choice - 1]
                
                # GUI I
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"\n{Fore.CYAN + Style.BRIGHT}{'═'*50}")
                    print(f"{Fore.CYAN + Style.BRIGHT}Department {selected_dept['department']}")
                    print(f"{Fore.CYAN + Style.BRIGHT}{'═'*50}")
                    print(f"{Fore.WHITE}• IP Address: {Fore.GREEN}{selected_dept['network_id']}/{selected_dept['subnet_cidr']}")
                    print(f"{Fore.WHITE}• VLAN Number: {Fore.GREEN}{selected_dept.get('vlan_number', 'N/A')}")
                    print(f"{Fore.WHITE}• VLAN Name: {Fore.GREEN}{selected_dept.get('vlan_name', 'N/A')}")
                    print(f"{Fore.WHITE}• Number of Host: {Fore.GREEN}{departments[selected_dept['department']]['hosts']}")
                    print(f"{Fore.WHITE}• Total Address (Including Network and Broadcast): {Fore.GREEN}{selected_dept['total_addresses']}")
                    print(f"{Fore.WHITE}• Range of Usable IP: {Fore.GREEN}{selected_dept['usable_range']}")
                    print(f"{Fore.WHITE}• Next Available: {Fore.GREEN}{selected_dept['next_available']}")
                    print(f"{Fore.WHITE}• Assignments:")
                    print(f"{Fore.WHITE}  └─ Router Interface: {Fore.GREEN}{selected_dept['router_ip']}")
                    print(f"{Fore.WHITE}  └─ Switch: {Fore.GREEN}{selected_dept['switch_ip']}")
                    print(f"{Fore.WHITE}  └─ End Devices: {Fore.GREEN}{selected_dept['end_devices_range']}")
                    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                    print(f"{Fore.CYAN + Style.BRIGHT}Action")
                    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                    print(f"{Fore.WHITE}• 1. Edit Department Name")
                    print(f"{Fore.WHITE}• 2. Edit VLAN")
                    print(f"{Fore.WHITE}• 3. Return to Map of IP Address Summary")
                    
                    action = input(f"{Fore.BLUE + Style.BRIGHT}➤ Select an action (1-3):\n{Fore.BLUE}> ").strip()
                    
                    if action == '1':
                        print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                        print(f"{Fore.CYAN + Style.BRIGHT}Edit Department Name")
                        print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                        while True:
                            new_name = input(f"{Fore.BLUE + Style.BRIGHT}➤ Please name the Department:\n{Fore.BLUE}> ").strip()
                            if new_name and new_name not in [d['department'] for d in subnet_details if d != selected_dept]:
                                old_name = selected_dept['department']
                                selected_dept['department'] = new_name
                                departments[new_name] = departments.pop(old_name)
                                break
                            print(f"{Fore.RED + Style.BRIGHT}✖ Department name must be unique and non-empty")
                    
                    elif action == '2' and vlan_choice == '1':
                        print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                        print(f"{Fore.CYAN + Style.BRIGHT}Edit VLAN")
                        print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
                        while True:
                            try:
                                vlan_num = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ Input VLAN number for Department {selected_dept['department']}:\n{Fore.BLUE}Number: > ").strip())
                                if vlan_num != 1 and vlan_num > 0:
                                    break
                                print(f"{Fore.RED + Style.BRIGHT}✖ VLAN number cannot be 1 and must be positive")
                            except ValueError:
                                print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
                        
                        vlan_name = input(f"{Fore.BLUE + Style.BRIGHT}Name: > ").strip()
                        if not vlan_name:
                            vlan_name = f"VLAN{vlan_num}"
                        selected_dept['vlan_number'] = vlan_num
                        selected_dept['vlan_name'] = vlan_name
                        departments[selected_dept['department']]['vlan_number'] = vlan_num
                        departments[selected_dept['department']]['vlan_name'] = vlan_name
                    
                    elif action == '3':
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid action")
            else:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid selection")
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")

if __name__ == "__main__":
    main()