import random

def print_header():
    print("\n" + "="*50)
    print("Script Title: IPv4 Subnet Calculator (Multiple Subnets)")
    print("Author: JOIBOI")
    print("="*50 + "\n")

# Helper function to convert IP address to integer
def ip_to_int(ip):
    return sum([int(octet) << (24 - 8 * i) for i, octet in enumerate(ip.split("."))])

# Helper function to convert integer to IP address
def int_to_ip(ip_int):
    return ".".join([str((ip_int >> (24 - 8 * i)) & 255) for i in range(4)])

# Parse subnet mask or CIDR input
def parse_mask_or_cidr(input_str):
    if input_str.startswith("/"):
        cidr = int(input_str[1:])
        if 0 <= cidr <= 32:
            return cidr
        raise ValueError("Invalid CIDR notation. Must be between 0 and 32.")
    else:
        octets = input_str.split('.')
        if len(octets) != 4 or not all(octet.isdigit() and 0 <= int(octet) <= 255 for octet in octets):
            raise ValueError("Invalid subnet mask format. Use xxx.xxx.xxx.xxx.")
        binary = "".join([bin(int(octet))[2:].zfill(8) for octet in octets])
        if "0" in binary and "1" in binary[binary.index("0"):]:
            raise ValueError("Invalid subnet mask: non-contiguous 1s.")
        cidr = binary.count("1")
        return cidr

# Convert CIDR to subnet mask
def cidr_to_mask(cidr):
    mask = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
    return int_to_ip(mask)

# Convert subnet mask or IP to binary notation
def to_binary(ip_or_mask):
    return ".".join([bin(int(octet))[2:].zfill(8) for octet in ip_or_mask.split(".")])

# Calculate subnet details based on base IP integer and CIDR
def calculate_subnet_details(base_ip_int, cidr):
    subnet_size = 1 << (32 - cidr)  # 2^(32 - cidr)
    network_int = base_ip_int & ~(subnet_size - 1)  # Align to subnet boundary
    broadcast_int = network_int + subnet_size - 1
    possible_addresses = subnet_size

    if cidr <= 30:
        usable_start = network_int + 1
        usable_end = broadcast_int - 1
        num_usable = usable_end - usable_start + 1
    elif cidr == 31:
        usable_start = network_int
        usable_end = broadcast_int
        num_usable = 2
    else:  # cidr == 32
        usable_start = network_int
        usable_end = network_int
        num_usable = 1

    return {
        "network": int_to_ip(network_int),
        "broadcast": int_to_ip(broadcast_int),
        "usable_start": int_to_ip(usable_start),
        "usable_end": int_to_ip(usable_end),
        "num_usable": num_usable,
        "possible_addresses": possible_addresses,
        "usable_addresses": num_usable,
        "next_base": network_int + subnet_size,
        "cidr": cidr,
        "mask": cidr_to_mask(cidr)
    }

# Generate IP addresses for devices
def generate_usable_ips(usable_start, usable_end, num_devices, mode):
    all_ips = [int_to_ip(ip_int) for ip_int in range(ip_to_int(usable_start), ip_to_int(usable_end) + 1)]
    if mode == "1":  # Randomized
        random.shuffle(all_ips)
    return all_ips[:num_devices]

# Main function
def main():
    print_header()
    
    # Get base IP address
    while True:
        print("Please Enter the IP Address:")
        base_ip = input("> ")
        try:
            octets = base_ip.split('.')
            if len(octets) == 4 and all(octet.isdigit() and 0 <= int(octet) <= 255 for octet in octets):
                break
            print("Invalid IP address. Please enter in the format xxx.xxx.xxx.xxx.")
        except ValueError:
            print("Invalid IP address.")

    # Choose input type: Subnet or CIDR
    while True:
        print("\nSubnet (1) or CIDR (2)?")
        choice = input("> ")
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Enter 1 for Subnet or 2 for CIDR.")

    # Get number of subnets
    while True:
        try:
            print("\nHow many multiple subnets on a network?")
            num_subnets = int(input("> "))
            if num_subnets > 0:
                break
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Enter a whole number.")

    # Collect subnet masks or CIDRs
    subnets = []
    current_ip_int = ip_to_int(base_ip)
    for i in range(num_subnets):
        subnet_letter = chr(65 + i)  # A, B, C, etc.
        while True:
            try:
                prompt = f"\nSubnet {subnet_letter}: " + ("Enter subnet mask: " if choice == "1" else "Enter CIDR (e.g., /24): ")
                print(prompt)
                input_str = input("> ")
                cidr = parse_mask_or_cidr(input_str)
                
                # Calculate subnet details
                details = calculate_subnet_details(current_ip_int, cidr)
                
                # Check if subnet exceeds Class C boundary (for 192.168.100.0/24)
                if ip_to_int(details["broadcast"]) > ip_to_int("192.168.100.255"):
                    print("Subnet exceeds Class C range (192.168.100.0/24). Try a smaller subnet.")
                    continue
                
                subnets.append(details)
                current_ip_int = details["next_base"]
                break
            except ValueError as e:
                print(e)

        # Display equivalent CIDR or subnet mask and binary notation
        if choice == "1":
            print(f"\nEquivalent CIDR: /{details['cidr']}")
            print(f"Binary Notation: {to_binary(details['mask'])}")
        else:
            print(f"\nEquivalent Subnet Mask: {details['mask']}")
            print(f"Binary Notation: {to_binary(details['mask'])}")

    # Display results
    print("\n" + "="*50)
    print("SUBNET CALCULATION RESULTS")
    print("="*50)
    
    # Process each subnet
    for i, details in enumerate(subnets):
        subnet_letter = chr(65 + i)
        print(f"\nSubnet {subnet_letter}:")
        print(f"├─ Subnet Mask: {details['mask']} | CIDR: /{details['cidr']}")
        print(f"├─ Possible Address (2^n): {details['possible_addresses']}")
        print(f"├─ Usable Address (2^n-2): {details['usable_addresses']}")
        print(f"├─ Network Address: {details['network']}")
        print(f"├─ Broadcast Address: {details['broadcast']}")
        print(f"├─ Range of Usable Address: {details['usable_start']} - {details['usable_end']}")
        print(f"└─ Number of Usable Address: {details['num_usable']}")

        # Get assignment mode for this subnet
        while True:
            print("\nRandomized (1) or Sequence (2)?")
            mode = input("> ")
            if mode in ["1", "2"]:
                break
            print("Invalid choice. Enter 1 for Randomized or 2 for Sequence.")

        # Get number of devices for this subnet
        while True:
            try:
                print(f"Enter number of devices for Subnet {subnet_letter}:")
                num_devices = int(input("> "))
                if 0 <= num_devices <= details['num_usable']:
                    break
                print(f"Number must be between 0 and {details['num_usable']}.")
            except ValueError:
                print("Invalid input. Enter a whole number.")

        # Assign IPs
        if num_devices > 0:
            ips = generate_usable_ips(details['usable_start'], details['usable_end'], num_devices, mode)
            for j, ip in enumerate(ips, 1):
                print(f"   └─ IP {chr(64 + j)}: {ip}")

if __name__ == "__main__":
    main()