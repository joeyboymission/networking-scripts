import ipaddress
import math
import os
from colorama import init, Fore, Style
import pyperclip  # Added for clipboard functionality

# Initialize colorama for cross-platform color support
init(autoreset=True)

def validate_ip(ip_str):
    """Validate an IPv4 address."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid IP address format (e.g., 172.30.240.0)")
        return False

def validate_subnet_mask(mask_str):
    """Validate a subnet mask (e.g., 255.255.252.0)."""
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
    """Convert subnet mask to CIDR notation."""
    try:
        mask_parts = mask.split('.')
        binary = ''.join(format(int(x), '08b') for x in mask_parts)
        return sum(1 for bit in binary if bit == '1')
    except:
        return None

def cidr_to_mask(cidr):
    """Convert CIDR notation to subnet mask."""
    try:
        # Create a subnet with the given CIDR
        subnet = ipaddress.IPv4Network(f"0.0.0.0/{cidr}", strict=False)
        # Return the subnet mask as a string
        return str(subnet.netmask)
    except:
        return None

def calculate_subnet_details(base_ip, cidr, departments):
    """Calculate subnet details using VLSM, inspired by C++ reference."""
    try:
        parent_network = ipaddress.ip_network(f"{base_ip}/{cidr}", strict=False)
        results = []
        
        # Precompute subnet sizes (powers of 2)
        subnet_sizes = [2**i for i in range(1, 15)]  # [2, 4, 8, ..., 16384]
        
        # Sort departments by host count (largest to smallest)
        sorted_depts = sorted(departments.items(), key=lambda x: x[1]['hosts'], reverse=True)
        
        current_address = parent_network.network_address
        
        for dept_name, dept_info in sorted_depts:
            # Calculate required addresses (hosts + network + broadcast)
            hosts_needed = dept_info['hosts'] + 2
            
            # Find smallest subnet size that accommodates hosts_needed
            subnet_size = None
            for size in subnet_sizes:
                if hosts_needed <= size:
                    subnet_size = size
                    break
            if subnet_size is None:
                print(f"{Fore.RED + Style.BRIGHT}✖ Host count for {dept_name} too large")
                return None
            
            # Calculate CIDR
            subnet_bits = int(math.log2(subnet_size))
            subnet_cidr = 32 - subnet_bits
            
            # Check if enough address space remains
            if int(current_address) + subnet_size > int(parent_network.broadcast_address) + 1:
                print(f"{Fore.RED + Style.BRIGHT}✖ Insufficient address space for {dept_name}")
                return None
            
            # Create subnet
            subnet = ipaddress.ip_network(f"{current_address}/{subnet_cidr}", strict=False)
            subnet_mask = cidr_to_mask(subnet_cidr)
            
            # Store department details
            dept_details = {
                'department': dept_name,
                'vlan_number': dept_info.get('vlan_number', 'None'),
                'vlan_name': dept_info.get('vlan_name', 'None'),
                'network_id': str(subnet.network_address),
                'broadcast': str(subnet.broadcast_address),
                'total_addresses': subnet_size,
                'usable_addresses': subnet_size - 2 if subnet_size > 2 else 0,
                'total_range': f"{subnet.network_address} - {subnet.broadcast_address}",
                'usable_range': f"{subnet[1]} - {subnet[-2]}" if subnet_size > 2 else "N/A",
                'router_ip': str(subnet[1]) if subnet_size > 2 else "N/A",
                'switch_ip': str(subnet[2]) if subnet_size > 3 else "N/A",
                'end_devices_range': f"{subnet[3]} - {subnet[-2]}" if subnet_size > 4 else "N/A",
                'next_available': str(subnet.broadcast_address + 1),
                'subnet_cidr': subnet_cidr,
                'subnet_mask': subnet_mask,
                'num_hosts': dept_info['hosts']
            }
            
            results.append(dept_details)
            current_address = subnet.broadcast_address + 1
        
        # Validate total addresses
        total_used = sum(detail['total_addresses'] for detail in results)
        if total_used > 2**(32 - cidr):
            print(f"{Fore.RED + Style.BRIGHT}✖ Total addresses ({total_used}) exceed available ({2**(32-cidr)})")
            return None
        
        return results
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}✖ Error in subnet calculation: {e}")
        return None

def generate_dept_details_text(selected_dept):
    """Generate text representation of department details for display and clipboard."""
    details = [
        f"Department {selected_dept['department']}",
        f"IP Address: {selected_dept['network_id']}/{selected_dept['subnet_cidr']}",
        f"Subnet Mask: {selected_dept['subnet_mask']}",
        f"VLAN Number: {selected_dept['vlan_number']}",
        f"VLAN Name: {selected_dept['vlan_name']}",
        f"Number of Host: {selected_dept['num_hosts']}",
        f"Total Address: {selected_dept['total_addresses']}",
        f"Network Address: {selected_dept['network_id']}",
        f"Broadcast Address: {selected_dept['broadcast']}",
        f"Range of Total IP: {selected_dept['total_range']}",
        f"Range of Usable IP: {selected_dept['usable_range']}",
        f"Next Available: {selected_dept['next_available']}",
        f"Assignments:",
        f"  - Router Interface: {selected_dept['router_ip']}",
        f"  - Switch: {selected_dept['switch_ip']}",
        f"  - End Devices: {selected_dept['end_devices_range']}"
    ]
    return "\n".join(details)

def main():
    departments = {}
    
    # GUI A: IP Address Input
    print(f"\n{Fore.CYAN + Style.BRIGHT}{'═'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}NUMBER OF HOST SUBNETTING CALCULATOR (IPv4)")
    print(f"{Fore.CYAN + Style.BRIGHT}{'═'*50}")
    print(f"{Fore.BLUE + Style.BRIGHT}➤ Enter the IP Address:")
    while True:
        ip_input = input(f"{Fore.BLUE}> ").strip()
        if validate_ip(ip_input):
            base_ip = ip_input
            break
    
    # GUI B: Subnet Mask or CIDR Selection
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Select Subnet Mask or CIDR")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.WHITE}• 1. Subnet Mask")
    print(f"{Fore.WHITE}• 2. CIDR")
    while True:
        choice = input(f"{Fore.BLUE + Style.BRIGHT}➤ Enter your choice (1-2):\n{Fore.BLUE}> ").strip()
        if choice == '1':
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}Subnet Mask Input")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            while True:
                subnet_mask = input(f"{Fore.BLUE + Style.BRIGHT}➤ Enter the Subnet Mask (e.g., 255.255.252.0):\n{Fore.BLUE}> ").strip()
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
    
    # GUI C: Number of Departments
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Number of Departments")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    while True:
        try:
            num_depts = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ How many departments are required:\n{Fore.BLUE}> ").strip())
            if num_depts > 0:
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Number must be positive")
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
    
    # GUI D: Department Naming
    dept_names = []
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Department Naming")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    for i in range(num_depts):
        while True:
            dept_name = input(f"{Fore.BLUE + Style.BRIGHT}➤ Name Department ({i+1} of {num_depts}):\n{Fore.BLUE}> ").strip()
            if dept_name and dept_name not in dept_names:
                dept_names.append(dept_name)
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Department name must be unique and non-empty")
    
    # GUI E: Number of Hosts per Department
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Number of Hosts per Department")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    for dept_name in dept_names:
        while True:
            try:
                hosts = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ How many hosts for Department {dept_name}:\n{Fore.BLUE}> ").strip())
                if hosts > 0:
                    departments[dept_name] = {'hosts': hosts}
                    break
                print(f"{Fore.RED + Style.BRIGHT}✖ Number of hosts must be positive")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
    
    # GUI F: VLAN Configuration
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}VLAN Configuration")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.WHITE}• 1. Yes")
    print(f"{Fore.WHITE}• 2. No")
    while True:
        vlan_choice = input(f"{Fore.BLUE + Style.BRIGHT}➤ Do departments have VLANs? (1-2):\n{Fore.BLUE}> ").strip()
        if vlan_choice in ['1', '2']:
            break
        print(f"{Fore.RED + Style.BRIGHT}✖ Please select 1 or 2")
    
    if vlan_choice == '1':
        print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        print(f"{Fore.CYAN + Style.BRIGHT}VLAN Number and Name Assignment")
        print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
        for dept_name in dept_names:
            while True:
                try:
                    vlan_num = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ VLAN number for Department {dept_name}:\n{Fore.BLUE}> ").strip())
                    if vlan_num != 1 and vlan_num > 0:
                        break
                    print(f"{Fore.RED + Style.BRIGHT}✖ VLAN number cannot be 1 and must be positive")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
            
            vlan_name = input(f"{Fore.BLUE + Style.BRIGHT}➤ VLAN name (Enter for VLAN{vlan_num}):\n{Fore.BLUE}> ").strip()
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
            print(f"{Fore.WHITE}• {i}. Department {Fore.GREEN}{detail['department']} ({detail['usable_addresses']} usable hosts)")
        print(f"{Fore.WHITE}• {len(subnet_details) + 1}. End the Program")
        
        try:
            choice = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ Select a department:\n{Fore.BLUE}> ").strip())
            if choice == len(subnet_details) + 1:
                # Add confirmation before ending the program
                confirm = input(f"{Fore.YELLOW + Style.BRIGHT}➤ Are you sure you want to end the program? (yes/no):\n{Fore.BLUE}> ").strip().lower()
                if confirm in ['yes', 'y']:
                    print(f"\n{Fore.CYAN + Style.BRIGHT}✔ Program ended.")
                    break
                continue
            
            if 1 <= choice <= len(subnet_details):
                selected_dept = subnet_details[choice - 1]
                
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"\n{Fore.CYAN + Style.BRIGHT}{'═'*50}")
                    print(f"{Fore.CYAN + Style.BRIGHT}Department {selected_dept['department']}")
                    print(f"{Fore.CYAN + Style.BRIGHT}{'═'*50}")
                    print(f"{Fore.WHITE}• IP Address: {Fore.GREEN}{selected_dept['network_id']}/{selected_dept['subnet_cidr']}")
                    print(f"{Fore.WHITE}• Subnet Mask: {Fore.GREEN}{selected_dept['subnet_mask']}")
                    print(f"{Fore.WHITE}• VLAN Number: {Fore.GREEN}{selected_dept['vlan_number']}")
                    print(f"{Fore.WHITE}• VLAN Name: {Fore.GREEN}{selected_dept['vlan_name']}")
                    print(f"{Fore.WHITE}• Number of Host: {Fore.GREEN}{selected_dept['num_hosts']}")
                    print(f"{Fore.WHITE}• Total Address: {Fore.GREEN}{selected_dept['total_addresses']}")
                    print(f"{Fore.WHITE}• Network Address: {Fore.GREEN}{selected_dept['network_id']}")
                    print(f"{Fore.WHITE}• Broadcast Address: {Fore.GREEN}{selected_dept['broadcast']}")
                    print(f"{Fore.WHITE}• Range of Total IP: {Fore.GREEN}{selected_dept['total_range']}")
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
                    print(f"{Fore.WHITE}• 3. Copy to Clipboard")
                    print(f"{Fore.WHITE}• 4. Return to Map of IP Address Summary")
                    
                    action = input(f"{Fore.BLUE + Style.BRIGHT}➤ Select an action (1-4):\n{Fore.BLUE}> ").strip()
                    
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
                                vlan_num = int(input(f"{Fore.BLUE + Style.BRIGHT}➤ Input VLAN number for Department {selected_dept['department']}:\n{Fore.BLUE}> ").strip())
                                if vlan_num != 1 and vlan_num > 0:
                                    break
                                print(f"{Fore.RED + Style.BRIGHT}✖ VLAN number cannot be 1 and must be positive")
                            except ValueError:
                                print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")
                        
                        vlan_name = input(f"{Fore.BLUE + Style.BRIGHT}➤ VLAN name (Enter for VLAN{vlan_num}):\n{Fore.BLUE}> ").strip()
                        if not vlan_name:
                            vlan_name = f"VLAN{vlan_num}"
                        selected_dept['vlan_number'] = vlan_num
                        selected_dept['vlan_name'] = vlan_name
                        departments[selected_dept['department']]['vlan_number'] = vlan_num
                        departments[selected_dept['department']]['vlan_name'] = vlan_name
                    
                    elif action == '3':
                        # Copy department details to clipboard
                        details_text = generate_dept_details_text(selected_dept)
                        try:
                            pyperclip.copy(details_text)
                            print(f"\n{Fore.GREEN + Style.BRIGHT}✔ Department details copied to clipboard!")
                            input(f"{Fore.BLUE + Style.BRIGHT}Press Enter to continue...")
                        except Exception as e:
                            print(f"\n{Fore.RED + Style.BRIGHT}✖ Failed to copy to clipboard: {e}")
                            input(f"{Fore.BLUE + Style.BRIGHT}Press Enter to continue...")
                    
                    elif action == '4':
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid action")
            else:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid selection")
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Please enter a valid number")

if __name__ == "__main__":
    main()