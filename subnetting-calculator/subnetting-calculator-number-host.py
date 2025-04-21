import ipaddress
import math

def get_ip_address(prompt):
    while True:
        try:
            ip = input(prompt)
            ipaddress.IPv4Address(ip)
            return ip
        except ipaddress.AddressValueError:
            print("Invalid IPv4 address. Please try again.")

def get_subnet_mask(prompt):
    while True:
        mask = input(prompt)
        try:
            ipaddress.IPv4Network(('0.0.0.0', mask), strict=False)
            return mask
        except ValueError:
            print("Invalid subnet mask. Please try again.")

def get_cidr(prompt):
    while True:
        cidr = input(prompt)
        if cidr.startswith('/') and cidr[1:].isdigit():
            n = int(cidr[1:])
            if 0 <= n <= 32:
                return n
        print("Invalid CIDR. Please enter /n where n is 0 to 32.")

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_non_negative_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Please enter a non-negative integer.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def calculate_subnet_details(base_net, departments):
    departments.sort(key=lambda x: x['hosts'] + 2, reverse=True)
    current_address = base_net.network_address
    for dept in departments:
        required_total = dept['hosts'] + 2
        m = math.ceil(math.log2(required_total))
        prefix_length = 32 - m
        subnet = ipaddress.ip_network((current_address, prefix_length), strict=False)
        dept['subnet'] = subnet
        current_address = subnet.broadcast_address + 1
        if current_address > base_net.broadcast_address:
            print(f"Warning: Subnet allocation for {dept['name']} exceeds base network capacity.")
            break

def main():
    # GUI A
    print("-------------------------------------------")
    print("NUMBER OF HOST SUBNETTING CALCULATOR (IPv4)")
    print("-------------------------------------------")
    ip = get_ip_address("Enter the IP Address\n>")

    print("Select which Subnet Mask or CIDR?")
    print("1. Subnet Mask")
    print("2. CIDR")
    while True:
        choice = input(">")
        if choice == '1':
            # GUI B1
            mask = get_subnet_mask("Enter the Subnet Mask (format 255.255.255.255)\n>")
            base_net = ipaddress.ip_network((ip, mask), strict=False)
            break
        elif choice == '2':
            # GUI B2
            cidr = get_cidr("Enter the CIDR (/n where n is the given number of bits)\n>")
            base_net = ipaddress.ip_network((ip, cidr), strict=False)
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

    # GUI C
    num_depts = get_positive_integer("How many area/departments/partition does required\n>")

    # Collect department information
    departments = []
    for i in range(num_depts):
        # GUI D
        name = input(f"Please name the Department ({i+1} of {num_depts})\n>")
        # GUI E
        hosts = get_non_negative_integer(f"How many host on Department {name}\n>")
        departments.append({'name': name, 'hosts': hosts})

    # GUI F
    print("Does every department/buildings have their own VLAN?")
    print("1. Yes")
    print("2. No")
    while True:
        choice = input(">")
        if choice == '1':
            has_vlan = True
            break
        elif choice == '2':
            has_vlan = False
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

    # GUI G1 and G1.1 if VLANs are selected
    if has_vlan:
        used_vlans = set()
        for dept in departments:
            while True:
                try:
                    vlan_num = int(input(f"Input VLAN number for Department {dept['name']}\nNumber: >"))
                    if vlan_num <= 1:
                        print("VLAN number must be greater than 1.")
                    elif vlan_num in used_vlans:
                        print("VLAN number already used. Please choose another.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            used_vlans.add(vlan_num)
            vlan_name = input("Name: >")
            dept['vlan_num'] = vlan_num
            dept['vlan_name'] = vlan_name

    # Calculate subnets
    calculate_subnet_details(base_net, departments)

    # GUI H and GUI I loop
    while True:
        print("-------------------------------------------")
        print("MAPPING OF IP ADDRESS SUMMARY")
        print("-------------------------------------------")
        for i, dept in enumerate(departments, 1):
            print(f"{i}. Department {dept['name']}")
        print(f"{len(departments)+1}. End the Program")
        try:
            choice = int(input("Please select which departments/building:\n>"))
            if 1 <= choice <= len(departments):
                dept = departments[choice-1]
                subnet = dept['subnet']
                total_possible = subnet.num_addresses
                usable_ips = max(total_possible - 2, 0)
                usable_range = f"{subnet.network_address + 1} to {subnet.broadcast_address - 1}" if total_possible > 2 else "None"
                next_available = subnet.broadcast_address + 1

                # GUI I
                print(f"Department {dept['name']}")
                print(f"Number of Host: {dept['hosts']}")
                print(f"Total Address (Including Network and Broadcast): {total_possible}")
                print(f"Range of Usable IP: {usable_range}")
                print(f"Next Available: {next_available}")
                print(f"Network ID: {subnet.network_address}")
                print(f"Broadcast ID: {subnet.broadcast_address}")
                print(f"Total Possible IP Addresses: {total_possible}")
                print(f"Total Usable IP Addresses: {usable_ips}")
                print("Assignments:")
                if total_possible > 2:
                    print(f"- Router Interface: {subnet.network_address + 1}")
                    print(f"- Switch: {subnet.network_address + 2}")
                    print(f"- End Devices: {subnet.network_address + 3} to {subnet.broadcast_address - 1}")
                else:
                    print("No usable IP addresses")
                if has_vlan:
                    print(f"VLAN: {dept['vlan_num']} ({dept['vlan_name']})")

                # Action options
                print("\nAction:")
                print("1. Edit Department Name")
                if has_vlan:
                    print("2. Edit VLAN")
                print("3. Return to Map of IP Address Summary")
                while True:
                    action = input(">")
                    if action == '1':
                        dept['name'] = input("Please name the Department\n>")
                        break
                    elif has_vlan and action == '2':
                        while True:
                            try:
                                new_vlan_num = int(input(f"Input VLAN number for Department {dept['name']}\nNumber: >"))
                                if new_vlan_num <= 1:
                                    print("VLAN number must be greater than 1.")
                                elif new_vlan_num in [d['vlan_num'] for d in departments if d != dept]:
                                    print("VLAN number already used. Please choose another.")
                                else:
                                    break
                            except ValueError:
                                print("Invalid input. Please enter an integer.")
                        dept['vlan_num'] = new_vlan_num
                        dept['vlan_name'] = input("Name: >")
                        break
                    elif action == '3':
                        break
                    else:
                        print("Invalid choice.")
            elif choice == len(departments) + 1:
                print("Ending the program.")
                return
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

if __name__ == "__main__":
    main()