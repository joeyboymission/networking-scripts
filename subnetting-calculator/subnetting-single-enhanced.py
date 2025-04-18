import random

def print_header():
    print("\n" + "="*50)
    print("Script Title: IPv4 Subnet Calculator (Single Subnet)")
    print("Author: JOIBOI")
    print("="*50 + "\n")

def to_binary(ip):
    return ".".join([bin(int(octet))[2:].zfill(8) for octet in ip.split(".")])

def mask_to_cidr(subnet_mask):
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in subnet_mask.split(".")])
    if "0" in binary and "1" in binary[binary.index("0"):]:
        raise ValueError("Invalid subnet mask: bits must be contiguous.")
    return sum([1 for bit in binary if bit == "1"])

def cidr_to_mask(cidr):
    mask = [0] * 32
    for i in range(cidr):
        mask[i] = 1
    mask = [str(sum([bit << (7 - j) for j, bit in enumerate(mask[i:i+8])])) for i in range(0, 32, 8)]
    return ".".join(mask)

def calculate_network_broadcast(ip, cidr):
    ip_octets = [int(octet) for octet in ip.split(".")]
    mask_octets = [int(octet) for octet in cidr_to_mask(cidr).split(".")]
    network = [ip_octets[i] & mask_octets[i] for i in range(4)]
    broadcast = [network[i] | (255 - mask_octets[i]) for i in range(4)]
    return ".".join(map(str, network)), ".".join(map(str, broadcast))

def usable_ip_range(network, broadcast):
    network_octets = [int(octet) for octet in network.split(".")]
    broadcast_octets = [int(octet) for octet in broadcast.split(".")]
    first_usable = network_octets[:]
    first_usable[-1] += 1
    last_usable = broadcast_octets[:]
    last_usable[-1] -= 1
    return ".".join(map(str, first_usable)), ".".join(map(str, last_usable))

def generate_usable_ips(first_usable, last_usable, num_devices, mode, max_usable):
    if num_devices > max_usable:
        raise ValueError(f"Requested {num_devices} devices, but only {max_usable} usable IPs available.")
    first = [int(octet) for octet in first_usable.split(".")]
    last = [int(octet) for octet in last_usable.split(".")]
    first_int = sum([first[i] << (24 - 8 * i) for i in range(4)])
    last_int = sum([last[i] << (24 - 8 * i) for i in range(4)])
    all_ips = [f"{(ip >> 24) & 255}.{(ip >> 16) & 255}.{(ip >> 8) & 255}.{ip & 255}" 
               for ip in range(first_int, last_int + 1)]
    if mode == "1":
        random.shuffle(all_ips)
        return all_ips[:num_devices]
    return all_ips[:num_devices]

def subnet_details(ip, cidr):
    subnet_mask = cidr_to_mask(cidr)
    binary = to_binary(subnet_mask)
    host_bits = 32 - cidr
    possible_addresses = 2 ** host_bits
    usable_addresses = possible_addresses - 2 if possible_addresses > 2 else 0
    network, broadcast = calculate_network_broadcast(ip, cidr)
    first_usable, last_usable = usable_ip_range(network, broadcast)
    ip_class = "A" if int(ip.split(".")[0]) <= 126 else "B" if int(ip.split(".")[0]) <= 191 else "C"
    default_cidr = 8 if ip_class == "A" else 16 if ip_class == "B" else 24
    borrowed_bits = cidr - default_cidr
    num_subnets = 2 ** borrowed_bits if borrowed_bits >= 0 else 1
    
    affected_octet = (cidr - 1) // 8
    mask_octets = [int(o) for o in subnet_mask.split(".")]
    borrowed_in_octet = bin(mask_octets[affected_octet]).count("1") - (8 if affected_octet > default_cidr // 8 else default_cidr % 8)
    increment = 2 ** (8 - borrowed_in_octet) if borrowed_bits > 0 else 256
    
    base_network = ".".join(ip.split(".")[:default_cidr//8] + ["0"] * (4 - default_cidr//8))
    subnet_location = ((int(network.split(".")[affected_octet]) - int(base_network.split(".")[affected_octet])) // increment) + 1
    
    subnets = []
    base = [int(o) for o in base_network.split(".")]
    for i in range(num_subnets):
        subnet_start = base[:]
        third_octet_increase = (i * increment) % 256
        second_octet_increase = (i * increment) // 256
        subnet_start[affected_octet] += third_octet_increase
        subnet_start[affected_octet - 1] += second_octet_increase
        subnet_network = ".".join(map(str, subnet_start))
        subnet_broadcast = calculate_network_broadcast(subnet_network, cidr)[1]
        subnet_first_usable, subnet_last_usable = usable_ip_range(subnet_network, subnet_broadcast)
        subnets.append({
            "network": subnet_network,
            "broadcast": subnet_broadcast,
            "range": (subnet_first_usable, subnet_last_usable),
            "possible": possible_addresses,
            "usable": usable_addresses
        })
    
    return {
        "subnet_mask": subnet_mask,
        "binary": binary,
        "possible": possible_addresses,
        "usable": usable_addresses,
        "network": network,
        "broadcast": broadcast,
        "range": (first_usable, last_usable),
        "num_usable": usable_addresses,
        "num_subnets": num_subnets,
        "increment": increment,
        "subnet_location": subnet_location,
        "ip_class": ip_class,
        "default_cidr": default_cidr,
        "affected_octet": affected_octet,
        "subnets": subnets,
        "ip_binary": to_binary(ip)
    }

def long_method(ip, subnet_mask, cidr, network, broadcast):
    print("\n" + "-"*50)
    print("LONG METHOD")
    print("-"*50)
    print(f"Given IP Address: {ip}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    
    print("A. Finding the First IP Address (Network Address)")
    print("Solution:")
    print("Requirements:")
    print(f"IP Address: {ip}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    print("Step 1: Convert to Binary Notation")
    ip_binary = to_binary(ip)
    mask_binary = to_binary(subnet_mask)
    print(f"IP Address: {ip} -> {ip_binary}")
    print(f"Subnet Mask: {subnet_mask} -> {mask_binary}\n")
    print("Step 2: Perform Bitwise AND Operation")
    network_binary = ".".join([bin(int(a) & int(m))[2:].zfill(8) for a, m in zip(ip.split("."), subnet_mask.split("."))])
    print(f"{ip_binary}")
    print(f"{mask_binary}")
    print("-"*50)
    print(f"Result: {network_binary} -> {network}\n")
    
    print("B. Finding the Last IP Address (Broadcast Address)")
    print("Solution:")
    print("Requirements:")
    print(f"Network Address: {network}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    print("Step 1: Invert the Subnet Mask")
    inverted_mask_binary = ".".join([bin(255 - int(m))[2:].zfill(8) for m in subnet_mask.split(".")])
    print(f"Subnet Mask: {mask_binary}")
    print(f"Inverted: {inverted_mask_binary}\n")
    print("Step 2: Perform Bitwise OR Operation")
    broadcast_binary = ".".join([bin(int(n) | int(im, 2))[2:].zfill(8) for n, im in zip(network.split("."), inverted_mask_binary.split("."))])
    print(f"{network_binary}")
    print(f"{inverted_mask_binary}")
    print("-"*50)
    print(f"Result: {broadcast_binary} -> {broadcast}\n")
    
    print("RESULT:")
    print(f"First IP Address (Network Address): {network}")
    print(f"Last IP Address (Broadcast Address): {broadcast}")

def short_method(ip, subnet_mask, cidr, network, broadcast):
    print("\n" + "-"*50)
    print("SHORT METHOD")
    print("-"*50)
    print(f"Given IP Address: {ip}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    
    print("A. Finding the First IP Address (Network Address)")
    print("Solution:")
    print("Requirements:")
    print(f"IP Address: {ip}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    network_octets = []
    for i, (ip_octet, mask_octet) in enumerate(zip(ip.split("."), subnet_mask.split("."))):
        ip_octet, mask_octet = int(ip_octet), int(mask_octet)
        if mask_octet == 255:
            print(f"Octet {i+1}: Mask = 255, copy IP octet: {ip_octet}")
            network_octets.append(str(ip_octet))
        elif mask_octet == 0:
            print(f"Octet {i+1}: Mask = 0, set to 0")
            network_octets.append("0")
        else:
            result = ip_octet & mask_octet
            print(f"Octet {i+1}: {ip_octet} AND {mask_octet} = {result}")
            network_octets.append(str(result))
    print(f"Result: {network}\n")
    
    print("B. Finding the Last IP Address (Broadcast Address)")
    print("Solution:")
    print("Requirements:")
    print(f"Network Address: {network}")
    print(f"Subnet Mask: {subnet_mask}")
    print(f"CIDR: /{cidr}\n")
    broadcast_octets = []
    for i, (net_octet, mask_octet) in enumerate(zip(network.split("."), subnet_mask.split("."))):
        net_octet, mask_octet = int(net_octet), int(mask_octet)
        if mask_octet == 255:
            print(f"Octet {i+1}: Mask = 255, copy network octet: {net_octet}")
            broadcast_octets.append(str(net_octet))
        elif mask_octet == 0:
            print(f"Octet {i+1}: Mask = 0, set to 255")
            broadcast_octets.append("255")
        else:
            result = net_octet | (255 - mask_octet)
            print(f"Octet {i+1}: {net_octet} OR {255 - mask_octet} = {result}")
            broadcast_octets.append(str(result))
    print(f"Result: {broadcast}\n")
    
    print("RESULT:")
    print(f"First IP Address (Network Address): {network}")
    print(f"Last IP Address (Broadcast Address): {broadcast}")

def subnet_label(index):
    if index < 26:
        return chr(65 + index)  # A-Z
    else:
        return "A" + chr(65 + (index - 26))  # AA-AF

def main():
    print_header()
    while True:
        print("Please Enter the IP Address:")
        ip = input("> ")
        try:
            octets = ip.split('.')
            if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                break
            print("Invalid IP address. Enter four octets between 0 and 255.")
        except ValueError:
            print("Invalid IP address. Use dotted decimal format (e.g., 192.168.1.0).")
    
    while True:
        print("\nWhat type? Subnet (1) or CIDR (2):")
        choice = input("> ")
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Enter 1 for Subnet or 2 for CIDR.")
    
    if choice == "1":
        while True:
            print("\nEnter the Subnet:")
            subnet_mask = input("> ")
            try:
                octets = subnet_mask.split('.')
                if len(octets) != 4 or not all(0 <= int(octet) <= 255 for octet in octets):
                    print("Invalid subnet mask. Please enter a valid subnet mask (e.g., 255.255.255.0)")
                    continue
                cidr = mask_to_cidr(subnet_mask)
                break
            except ValueError as e:
                print(f"Error: {e}")
    else:
        while True:
            print("\nEnter the CIDR: /")
            try:
                cidr = int(input("> "))
                if 0 <= cidr <= 32:
                    subnet_mask = cidr_to_mask(cidr)
                    break
                print("Invalid CIDR. Enter a value between 0 and 32.")
            except ValueError:
                print("Invalid input. Enter a numeric CIDR value.")
    
    details = subnet_details(ip, cidr)
    print("\n" + "-"*50)
    print("NETWORK SUMMARY")
    print("-"*50)
    print(f"├─ Given IP Binary Notation: {details['ip_binary']}")
    print(f"├─ Given Subnet/CIDR Binary Notation: {details['binary']}")
    print(f"├─ First IP Address (Network Address): {details['network']}")
    print(f"├─ Last IP Address (Broadcast Address): {details['broadcast']}")
    print(f"├─ Total Number of Subnets (2^m): {details['num_subnets']}")
    print(f"├─ Total Number of Possible Addresses (2^n): {details['possible']}")
    print(f"├─ Total Number of Usable Address (2^n-2): {details['usable']}")
    print(f"├─ Subnet Steps: {details['increment']}")
    print(f"└─ Location of the IP Address on what Subnet: Subnet {details['subnet_location']}")
    
    while True:
        print("\nComputation Options:")
        print("What would you like me to do?")
        print("1. Assigned Usable IP Address")
        print("2. Solution For IP Binary Notation")
        print("3. Solution for Subnet/CIDR Binary Notation")
        print("4. Solution for First IP Address (Network Address)")
        print("5. Solution for Last IP Address (Broadcast Address)")
        print("6. Solution for Total Number of Subnets")
        print("7. Solution for Number of Possible Address")
        print("8. Solution for Total Number of Usable Address")
        print("9. Solution for Subnet Steps")
        print("10. Solution for the Location of the IP Address on what Subnet")
        print("11. End the program")
        choice = input("> ")
        
        if choice == "1":
            print("\n" + "-"*50)
            print("ASSIGNED USABLE IP ADDRESS")
            print("-"*50)
            print("Please specify how many devices:")
            try:
                num_devices = int(input("> "))
                if num_devices <= 0:
                    print("Enter a positive number of devices.")
                    continue
                print("Randomized (1) or Sequence (2):")
                mode = input("> ")
                if mode not in ["1", "2"]:
                    print("Invalid choice. Enter 1 for Randomized or 2 for Sequence.")
                    continue
                
                for i, subnet in enumerate(details['subnets']):
                    if i >= details['num_subnets']:
                        break
                    ips = generate_usable_ips(subnet['range'][0], subnet['range'][1], num_devices, mode, subnet['usable'])
                    print(f"\nSubnet {i + 1}:")
                    print(f"├─ Network Address: {subnet['network']}")
                    print(f"├─ Broadcast Address: {subnet['broadcast']}")
                    print(f"└─ Usable IP range: {subnet['range'][0]} - {subnet['range'][1]}")
                    for j, ip_addr in enumerate(ips, 1):
                        print(f"   └─ IP {chr(64 + j)}: {ip_addr}")
                input("\nPress Enter key to return to the Network Summary")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            print("\n" + "-"*50)
            print("IP BINARY NOTATION")
            print("-"*50)
            print(f"IP Address: {ip}")
            print("Solution:")
            print("Step 1: Convert each octet to 8-bit binary")
            binary = to_binary(ip)
            for i, (octet, bin_octet) in enumerate(zip(ip.split("."), binary.split(".")), 1):
                print(f"Octet {i}: {octet} -> {bin_octet}")
            print(f"Result: {binary}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "3":
            print("\n" + "-"*50)
            print("SUBNET/CIDR BINARY NOTATION")
            print("-"*50)
            print(f"Subnet Mask: {subnet_mask}")
            print(f"CIDR: /{cidr}")
            print("Solution:")
            print("Step 1: Convert each octet to 8-bit binary")
            binary = to_binary(subnet_mask)
            for i, (octet, bin_octet) in enumerate(zip(subnet_mask.split("."), binary.split(".")), 1):
                print(f"Octet {i}: {octet} -> {bin_octet}")
            print(f"Result: {binary}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "4":
            print("\n" + "-"*50)
            print("FIRST IP ADDRESS (NETWORK ADDRESS)")
            print("-"*50)
            print("What method?")
            print("1. Long Method")
            print("2. Short Method")
            method_choice = input("> ")
            if method_choice == "1":
                long_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            elif method_choice == "2":
                short_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            else:
                print("Invalid choice. Enter 1 or 2.")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "5":
            print("\n" + "-"*50)
            print("LAST IP ADDRESS (BROADCAST ADDRESS)")
            print("-"*50)
            print("What method?")
            print("1. Long Method")
            print("2. Short Method")
            method_choice = input("> ")
            if method_choice == "1":
                long_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            elif method_choice == "2":
                short_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            else:
                print("Invalid choice. Enter 1 or 2.")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "6":
            print("\n" + "-"*50)
            print("TOTAL NUMBER OF SUBNETS")
            print("-"*50)
            print("Solution:")
            print(f"IP Class: {details['ip_class']} (Default CIDR: /{details['default_cidr']})")
            print(f"Given CIDR: /{cidr}")
            print("Step 1: Calculate borrowed bits (m)")
            borrowed_bits = cidr - details['default_cidr']
            print(f"m = {cidr} - {details['default_cidr']} = {borrowed_bits}")
            print("Step 2: Calculate total subnets (2^m)")
            print(f"2^{borrowed_bits} = {details['num_subnets']}")
            print(f"Result: Total Number of Subnets = {details['num_subnets']}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "7":
            print("\n" + "-"*50)
            print("NUMBER OF POSSIBLE ADDRESSES")
            print("-"*50)
            print("Solution:")
            print(f"CIDR: /{cidr}")
            print("Step 1: Calculate host bits (n)")
            host_bits = 32 - cidr
            print(f"n = 32 - {cidr} = {host_bits}")
            print("Step 2: Calculate total possible addresses (2^n)")
            print(f"2^{host_bits} = {details['possible']}")
            print(f"Result: Number of Possible Addresses = {details['possible']}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "8":
            print("\n" + "-"*50)
            print("TOTAL NUMBER OF USABLE ADDRESSES")
            print("-"*50)
            print("Solution:")
            print(f"CIDR: /{cidr}")
            print("Step 1: Calculate total possible addresses")
            host_bits = 32 - cidr
            possible = 2 ** host_bits
            print(f"n = 32 - {cidr} = {host_bits}")
            print(f"2^{host_bits} = {possible}")
            print("Step 2: Subtract network and broadcast addresses")
            print(f"{possible} - 2 = {details['usable']}")
            print(f"Result: Total Number of Usable Addresses = {details['usable']}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "9":
            print("\n" + "-"*50)
            print("SUBNET STEPS")
            print("-"*50)
            print("Solution:")
            print(f"CIDR: /{cidr}")
            print(f"IP Class: {details['ip_class']} (Default CIDR: /{details['default_cidr']})")
            print("Step 1: Calculate borrowed bits (m)")
            borrowed_bits = cidr - details['default_cidr']
            print(f"m = {cidr} - {details['default_cidr']} = {borrowed_bits}")
            print(f"Step 2: Identify affected octet (octet {details['affected_octet'] + 1})")
            print(f"Subnet Mask: {subnet_mask}")
            print(f"Binary: {details['binary']}")
            print(f"Step 3: Calculate borrowed bits in affected octet")
            print(f"Borrowed bits in octet {details['affected_octet'] + 1}: {bin(int(subnet_mask.split('.')[details['affected_octet']])).count('1')}")
            print(f"Step 4: Calculate remaining host bits in affected octet")
            remaining_host_bits = 8 - bin(int(subnet_mask.split('.')[details['affected_octet']])).count('1')
            print(f"8 - {bin(int(subnet_mask.split('.')[details['affected_octet']])).count('1')} = {remaining_host_bits}")
            print(f"Step 5: Calculate increment (2^remaining host bits)")
            print(f"2^{remaining_host_bits} = {details['increment']}")
            print(f"Result: Subnet Steps = {details['increment']}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "10":
            print("\n" + "-"*50)
            print("LOCATION OF THE IP ADDRESS ON WHAT SUBNET")
            print("-"*50)
            print("Solution:")
            print(f"IP Address: {ip}")
            print(f"CIDR: /{cidr}")
            print(f"Network Address: {details['network']}")
            print(f"IP Class: {details['ip_class']} (Default CIDR: /{details['default_cidr']})")
            print("Step 1: Calculate borrowed bits (m)")
            borrowed_bits = cidr - details['default_cidr']
            print(f"m = {cidr} - {details['default_cidr']} = {borrowed_bits}")
            print("Step 2: Calculate subnet increment")
            print(f"Increment in octet {details['affected_octet'] + 1}: {details['increment']}")
            print("Step 3: Determine subnet location")
            base_octet = int(details['network'].split(".")[details['affected_octet']])
            print(f"Network octet {details['affected_octet'] + 1}: {base_octet}")
            print(f"Location = ({base_octet} ÷ {details['increment']}) + 1 = {details['subnet_location']}")
            print(f"Location: Subnet {details['subnet_location']}\n")
            print("Full List:")
            for i, subnet in enumerate(details['subnets']):
                print(f"Subnet {i + 1}: {subnet['network']} - {subnet['broadcast']}")
            input("\nPress Enter key to return to the Network Summary")
        
        elif choice == "11":
            print("Program ended.")
            break
        else:
            print("Invalid choice. Enter a number between 1 and 11.")

if __name__ == "__main__":
    main()