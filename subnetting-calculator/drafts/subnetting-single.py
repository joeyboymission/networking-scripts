import random

def print_header():
    print("\n" + "="*50)
    print("Script Title: IPv4 Subnet Calculator (Single Subnet)")
    print("Author: JOIBOI")
    print("="*50 + "\n")

# Function to convert IP or subnet mask to binary
def to_binary(ip):
    return ".".join([bin(int(octet))[2:].zfill(8) for octet in ip.split(".")])

# Function to convert subnet mask to CIDR notation
def mask_to_cidr(subnet_mask):
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in subnet_mask.split(".")])
    return sum([1 for bit in binary if bit == "1"])

# Function to convert CIDR to subnet mask
def cidr_to_mask(cidr):
    mask = [0] * 32
    for i in range(cidr):
        mask[i] = 1
    mask = [str(sum([bit << (7 - j) for j, bit in enumerate(mask[i:i+8])])) for i in range(0, 32, 8)]
    return ".".join(mask)

# Function to calculate network and broadcast addresses
def calculate_network_broadcast(ip, cidr):
    ip_octets = [int(octet) for octet in ip.split(".")]
    mask_octets = [int(octet) for octet in cidr_to_mask(cidr).split(".")]
    
    network = [ip_octets[i] & mask_octets[i] for i in range(4)]
    broadcast = [network[i] | (255 - mask_octets[i]) for i in range(4)]
    
    return ".".join(map(str, network)), ".".join(map(str, broadcast))

# Function to calculate usable IP range
def usable_ip_range(network, broadcast):
    network_octets = [int(octet) for octet in network.split(".")]
    broadcast_octets = [int(octet) for octet in broadcast.split(".")]
    
    first_usable = network_octets[:]
    first_usable[-1] += 1
    last_usable = broadcast_octets[:]
    last_usable[-1] -= 1
    
    return ".".join(map(str, first_usable)), ".".join(map(str, last_usable))

# Function to generate list of usable IPs
def generate_usable_ips(first_usable, last_usable, num_devices, mode):
    first = [int(octet) for octet in first_usable.split(".")]
    last = [int(octet) for octet in last_usable.split(".")]
    
    # Convert IPs to integer for easier manipulation
    first_int = sum([first[i] << (24 - 8 * i) for i in range(4)])
    last_int = sum([last[i] << (24 - 8 * i) for i in range(4)])
    
    all_ips = [f"{(ip >> 24) & 255}.{(ip >> 16) & 255}.{(ip >> 8) & 255}.{ip & 255}" 
               for ip in range(first_int, last_int + 1)]
    
    if mode == "1":  # Randomized
        random.shuffle(all_ips)
        return all_ips[:num_devices]
    else:  # Sequential
        return all_ips[:num_devices]

# Function to calculate subnet details
def subnet_details(ip, cidr):
    subnet_mask = cidr_to_mask(cidr)
    binary = to_binary(subnet_mask)
    host_bits = 32 - cidr
    possible_addresses = 2 ** host_bits
    usable_addresses = possible_addresses - 2 if possible_addresses > 2 else 0
    network, broadcast = calculate_network_broadcast(ip, cidr)
    first_usable, last_usable = usable_ip_range(network, broadcast)
    
    # Calculate number of subnets (assuming classful base for simplicity)
    ip_class = "A" if int(ip.split(".")[0]) <= 126 else "B" if int(ip.split(".")[0]) <= 191 else "C"
    default_cidr = 8 if ip_class == "A" else 16 if ip_class == "B" else 24
    borrowed_bits = cidr - default_cidr
    num_subnets = 2 ** borrowed_bits if borrowed_bits >= 0 else 1
    
    return {
        "subnet_mask": subnet_mask,
        "binary": binary,
        "possible": possible_addresses,
        "usable": usable_addresses,
        "network": network,
        "broadcast": broadcast,
        "range": (first_usable, last_usable),
        "num_usable": usable_addresses,
        "num_subnets": num_subnets
    }

# Main program
def main():
    print_header()
    
    while True:
        print("Please Enter the IP Address:")
        ip = input("> ")
        # Basic IP validation
        try:
            octets = ip.split('.')
            if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                break
            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1)")
        except ValueError:
            print("Invalid IP address. Please enter a valid IP address (e.g., 192.168.1.1)")
    
    while True:
        print("\nWhat type? Subnet (1) or CIDR (2):")
        choice = input("> ")
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 for Subnet or 2 for CIDR.")
    
    if choice == "1":
        while True:
            print("\nEnter the Subnet Mask:")
            subnet_mask = input("> ")
            try:
                octets = subnet_mask.split('.')
                if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                    cidr = mask_to_cidr(subnet_mask)
                    print(f"\nEquivalent CIDR: /{cidr}")
                    break
                print("Invalid subnet mask. Please enter a valid subnet mask (e.g., 255.255.255.0)")
            except ValueError:
                print("Invalid subnet mask. Please enter a valid subnet mask (e.g., 255.255.255.0)")
    elif choice == "2":
        while True:
            print("\nEnter the CIDR: /")
            try:
                cidr = int(input("> "))
                if 8 <= cidr <= 32:
                    subnet_mask = cidr_to_mask(cidr)
                    print(f"\nEquivalent Subnet Mask: {subnet_mask}")
                    break
                print("Invalid CIDR. Must be between 8 and 32.")
            except ValueError:
                print("Invalid input. Please enter a number between 8 and 32.")
    
    details = subnet_details(ip, cidr)
    print("\n" + "-"*50)
    print("SUBNET CALCULATION RESULTS")
    print("-"*50)
    print(f"Binary Notation: {details['binary']}\n")
    print(f"Network Details:")
    print(f"├─ Possible Address (2^n): {details['possible']}")
    print(f"├─ Usable Address (2^n-2): {details['usable']}")
    print(f"├─ Network Address: {details['network']}")
    print(f"├─ Broadcast Address: {details['broadcast']}")
    print(f"├─ Range of Usable Address: {details['range'][0]} - {details['range'][1]}")
    print(f"├─ Number of Usable Address: {details['num_usable']}")
    print(f"└─ Number of Subnet: {details['num_subnets']}")
    
    while True:
        print("\nPlease specify how many devices:")
        try:
            num_devices = int(input("> "))
            if 0 <= num_devices <= details['num_usable']:
                break
            print(f"Invalid number of devices. Must be between 0 and {details['num_usable']}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    while True:
        print("\nRandomized (1) or Sequence (2):")
        mode = input("> ")
        if mode in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 for Randomized or 2 for Sequence.")
    
    # Handle subnets
    if details['num_subnets'] > 1:
        subnet_size = details['possible']
        base_ip = [int(octet) for octet in details['network'].split(".")]
        for subnet_idx in range(details['num_subnets']):
            subnet_start = sum([base_ip[i] << (24 - 8 * i) for i in range(4)]) + subnet_idx * subnet_size
            subnet_end = subnet_start + subnet_size - 1
            network = f"{(subnet_start >> 24) & 255}.{(subnet_start >> 16) & 255}.{(subnet_start >> 8) & 255}.{subnet_start & 255}"
            broadcast = f"{(subnet_end >> 24) & 255}.{(subnet_end >> 16) & 255}.{(subnet_end >> 8) & 255}.{subnet_end & 255}"
            first_usable, last_usable = usable_ip_range(network, broadcast)
            print(f"\nSubnet {chr(65 + subnet_idx)}:")
            print(f"├─ Usable IP range: {first_usable} - {last_usable}")
            print(f"└─ Number of Usable Address: {details['usable']}")
            ips = generate_usable_ips(first_usable, last_usable, min(num_devices, details['usable']), mode)
            for i, ip in enumerate(ips, 1):
                print(f"   └─ IP {chr(64 + i)}: {ip}")
    else:
        print(f"\nSubnet:")
        print(f"├─ Usable IP range: {details['range'][0]} - {details['range'][1]}")
        print(f"└─ Number of Usable Address: {details['num_usable']}")
        ips = generate_usable_ips(details['range'][0], details['range'][1], num_devices, mode)
        for i, ip in enumerate(ips, 1):
            print(f"   └─ IP {chr(64 + i)}: {ip}")

if __name__ == "__main__":
    main()