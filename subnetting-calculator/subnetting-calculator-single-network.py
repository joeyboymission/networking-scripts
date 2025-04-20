import random
import math
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

def print_header():
    print(f"\n{Fore.CYAN + Style.BRIGHT}{'='*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Script Title: IPv4 Subnet Calculator")
    print(f"{Fore.CYAN + Style.BRIGHT}Author: JOIBOI")
    print(f"{Fore.CYAN + Style.BRIGHT}{'='*50}\n")

def to_binary(ip):
    return ".".join([bin(int(octet))[2:].zfill(8) for octet in ip.split(".")])

def ip_to_binary_str(ip):
    return "".join([bin(int(octet))[2:].zfill(8) for octet in ip.split(".")])

def ip_to_integer(ip):
    octets = [int(o) for o in ip.split(".")]
    return sum(octet << (24 - 8 * i) for i, octet in enumerate(octets))

def ip_to_hex(ip):
    return hex(ip_to_integer(ip))

def ip_to_in_addr_arpa(ip):
    return ".".join(reversed(ip.split("."))) + ".in-addr.arpa"

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

def wildcard_mask(subnet_mask):
    return ".".join([str(255 - int(octet)) for octet in subnet_mask.split(".")])

def get_ip_class(ip, cidr):
    if cidr >= 24:
        return "C"
    first_octet = int(ip.split(".")[0])
    if 0 <= first_octet <= 127:
        return "A"
    elif 128 <= first_octet <= 191:
        return "B"
    elif 192 <= first_octet <= 223:
        return "C"
    elif 224 <= first_octet <= 239:
        return "D"
    else:
        return "E"

def is_private_ip(ip):
    octets = [int(o) for o in ip.split(".")]
    if octets[0] == 10:
        return True
    if octets[0] == 172 and 16 <= octets[1] <= 31:
        return True
    if octets[0] == 192 and octets[1] == 168:
        return True
    return False

def is_special_ip(ip):
    octets = [int(o) for o in ip.split(".")]
    if octets[0] == 127:
        return "Loopback"
    if 224 <= octets[0] <= 239:
        return "Multicast"
    if octets[0] == 0 or octets[0] == 255:
        return "Reserved"
    return None

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

def subnet_details(ip, parent_cidr, cidr):
    subnet_mask = cidr_to_mask(cidr)
    binary = to_binary(subnet_mask)
    host_bits = 32 - cidr
    possible_addresses = 2 ** host_bits
    usable_addresses = possible_addresses - 2 if possible_addresses > 2 else 0
    network, broadcast = calculate_network_broadcast(ip, cidr)
    first_usable, last_usable = usable_ip_range(network, broadcast)
    
    # Calculate subnets based on parent network
    borrowed_bits = max(0, cidr - parent_cidr)
    num_subnets = 2 ** borrowed_bits if borrowed_bits > 0 else 1
    subnet_step = 2 ** (32 - cidr)
    
    # Calculate subnet location
    parent_network, _ = calculate_network_broadcast(ip, parent_cidr)
    parent_octets = [int(o) for o in parent_network.split(".")]
    network_octets = [int(o) for o in network.split(".")]
    parent_mask = [int(o) for o in cidr_to_mask(parent_cidr).split(".")]
    subnet_mask_octets = [int(o) for o in subnet_mask.split(".")]
    affected_octet_idx = next(i for i in range(4) if parent_mask[i] != subnet_mask_octets[i])
    bits_in_affected = bin(subnet_mask_octets[affected_octet_idx])[2:].count("1") - bin(parent_mask[affected_octet_idx])[2:].count("1")
    increment = 2 ** (8 - bits_in_affected)
    subnet_location = (network_octets[affected_octet_idx] // increment) + 1
    
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
        "subnet_location": subnet_location,
        "parent_cidr": parent_cidr,
        "subnet_step": subnet_step,
        "parent_network": parent_network,
        "ip_binary": ip_to_binary_str(ip),
        "integer_id": ip_to_integer(ip),
        "hex_id": ip_to_hex(ip),
        "in_addr_arpa": ip_to_in_addr_arpa(ip),
        "ip_class": get_ip_class(ip, cidr),
        "ip_type": "Private" if is_private_ip(ip) else ("Loopback" if is_special_ip(ip) == "Loopback" else "Public"),
        "wildcard_mask": wildcard_mask(subnet_mask)
    }

def long_method(ip, subnet_mask, cidr, network, broadcast):
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}LONG METHOD")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.GREEN}Given IP Address: {ip}")
    print(f"{Fore.GREEN}Subnet Mask: {subnet_mask}")
    print(f"{Fore.GREEN}CIDR: /{cidr}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}A. Finding the First IP Address (Network Address)")
    print(f"{Fore.WHITE}Solution:")
    print(f"{Fore.WHITE}Requirements:")
    print(f"{Fore.WHITE}└─ IP Address: {Fore.GREEN}{ip}")
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{subnet_mask}\n")
    print(f"{Fore.WHITE + Style.BRIGHT}Step 1: Convert to Binary Notation")
    ip_binary = to_binary(ip)
    mask_binary = to_binary(subnet_mask)
    print(f"{Fore.WHITE}└─ IP Address: {Fore.GREEN}{ip} → {ip_binary}")
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{subnet_mask} → {mask_binary}\n")
    ip_octets = ip.split(".")
    mask_octets = subnet_mask.split(".")
    print(f"{Fore.WHITE + Style.BRIGHT}Step 2: Perform Bitwise AND Operation")
    network_binary = []
    for i, (ip_octet, mask_octet) in enumerate(zip(ip_octets, mask_octets), 1):
        ip_bin = bin(int(ip_octet))[2:].zfill(8)
        mask_bin = bin(int(mask_octet))[2:].zfill(8)
        result_bin = bin(int(ip_octet) & int(mask_octet))[2:].zfill(8)
        result_dec = int(result_bin, 2)
        print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{ip_octet} ({ip_bin}) {Fore.WHITE}AND {Fore.GREEN}{mask_octet} ({mask_bin}) {Fore.WHITE}= {Fore.GREEN}{result_dec} ({result_bin})")
        network_binary.append(str(result_dec))
    network_binary_str = ".".join([bin(int(o))[2:].zfill(8) for o in network_binary])
    print(f"\n{Fore.WHITE}└─ Result: {Fore.GREEN}{network_binary_str} → {network}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}B. Finding the Last IP Address (Broadcast Address)")
    print(f"{Fore.WHITE}Solution:")
    print(f"{Fore.WHITE}Requirements:")
    print(f"{Fore.WHITE}└─ Network Address: {Fore.GREEN}{network}")
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{subnet_mask}\n")
    print(f"{Fore.WHITE + Style.BRIGHT}Step 1: Invert the Subnet Mask")
    inverted_mask = [str(255 - int(o)) for o in mask_octets]
    inverted_mask_binary = to_binary(".".join(inverted_mask))
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{mask_binary}")
    print(f"{Fore.WHITE}└─ Inverted Subnet Mask: {Fore.GREEN}{'.'.join(inverted_mask)} → {inverted_mask_binary}\n")
    print(f"{Fore.WHITE + Style.BRIGHT}Step 2: Perform Bitwise OR Operation")
    network_octets = network.split(".")
    broadcast_binary = []
    for i, (net_octet, inv_mask_octet) in enumerate(zip(network_octets, inverted_mask), 1):
        net_bin = bin(int(net_octet))[2:].zfill(8)
        inv_mask_bin = bin(int(inv_mask_octet))[2:].zfill(8)
        result_bin = bin(int(net_octet) | int(inv_mask_octet))[2:].zfill(8)
        result_dec = int(result_bin, 2)
        print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{net_octet} ({net_bin}) {Fore.WHITE}OR {Fore.GREEN}{inv_mask_octet} ({inv_mask_bin}) {Fore.WHITE}= {Fore.GREEN}{result_dec} ({result_bin})")
        broadcast_binary.append(str(result_dec))
    broadcast_binary_str = ".".join([bin(int(o))[2:].zfill(8) for o in broadcast_binary])
    print(f"\n{Fore.WHITE}└─ Result: {Fore.GREEN}{broadcast_binary_str} → {broadcast}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}RESULT:")
    print(f"{Fore.MAGENTA}✔ First IP Address (Network Address): {network}")
    print(f"{Fore.MAGENTA}✔ Last IP Address (Broadcast Address): {broadcast}")

def short_method(ip, subnet_mask, cidr, network, broadcast):
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}SHORT METHOD")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.GREEN}Given IP Address: {ip}")
    print(f"{Fore.GREEN}Subnet Mask: {subnet_mask}")
    print(f"{Fore.GREEN}CIDR: /{cidr}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}A. Finding the First IP Address (Network Address)")
    print(f"{Fore.WHITE}Solution:")
    print(f"{Fore.WHITE}Requirements:")
    print(f"{Fore.WHITE}└─ IP Address: {Fore.GREEN}{ip}")
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{subnet_mask}\n")
    ip_octets = ip.split(".")
    mask_octets = subnet_mask.split(".")
    network_octets = []
    for i, (ip_octet, mask_octet) in enumerate(zip(ip_octets, mask_octets), 1):
        ip_octet, mask_octet = int(ip_octet), int(mask_octet)
        if mask_octet == 255:
            print(f"{Fore.WHITE}├─ Octet {i}: Mask = 255, copy IP octet: {Fore.GREEN}{ip_octet}")
            network_octets.append(str(ip_octet))
        elif mask_octet == 0:
            print(f"{Fore.WHITE}├─ Octet {i}: Mask = 0, set to 0")
            network_octets.append("0")
        else:
            ip_bin = bin(ip_octet)[2:].zfill(8)
            mask_bin = bin(mask_octet)[2:].zfill(8)
            result = ip_octet & mask_octet
            result_bin = bin(result)[2:].zfill(8)
            print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{ip_octet} ({ip_bin}) {Fore.WHITE}AND {Fore.GREEN}{mask_octet} ({mask_bin}) {Fore.WHITE}= {Fore.GREEN}{result} ({result_bin})")
            network_octets.append(str(result))
    print(f"\n{Fore.WHITE}└─ Result: {Fore.GREEN}{network}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}B. Finding the Last IP Address (Broadcast Address)")
    print(f"{Fore.WHITE}Solution:")
    print(f"{Fore.WHITE}Requirements:")
    print(f"{Fore.WHITE}└─ Network Address: {Fore.GREEN}{network}")
    print(f"{Fore.WHITE}└─ Subnet Mask: {Fore.GREEN}{subnet_mask}\n")
    network_octets = network.split(".")
    broadcast_octets = []
    for i, (net_octet, mask_octet) in enumerate(zip(network_octets, mask_octets), 1):
        net_octet, mask_octet = int(net_octet), int(mask_octet)
        if mask_octet == 255:
            print(f"{Fore.WHITE}├─ Octet {i}: Mask = 255, copy network octet: {Fore.GREEN}{net_octet}")
            broadcast_octets.append(str(net_octet))
        elif mask_octet == 0:
            print(f"{Fore.WHITE}├─ Octet {i}: Mask = 0, set to 255")
            broadcast_octets.append("255")
        else:
            net_bin = bin(net_octet)[2:].zfill(8)
            inv_mask = 255 - mask_octet
            inv_mask_bin = bin(inv_mask)[2:].zfill(8)
            result = net_octet | inv_mask
            result_bin = bin(result)[2:].zfill(8)
            print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{net_octet} ({net_bin}) {Fore.WHITE}OR {Fore.GREEN}{inv_mask} ({inv_mask_bin}) {Fore.WHITE}= {Fore.GREEN}{result} ({result_bin})")
            broadcast_octets.append(str(result))
    print(f"\n{Fore.WHITE}└─ Result: {Fore.GREEN}{broadcast}\n")
    
    print(f"{Fore.WHITE + Style.BRIGHT}RESULT:")
    print(f"{Fore.MAGENTA}✔ First IP Address (Network Address): {network}")
    print(f"{Fore.MAGENTA}✔ Last IP Address (Broadcast Address): {broadcast}")

def generate_subnets(parent_network, parent_cidr, cidr, num_subnets):
    subnets = []
    base = [int(o) for o in parent_network.split(".")]
    subnet_step = 2 ** (32 - cidr)
    
    for i in range(num_subnets):
        subnet_start = base[:]
        subnet_start[3] += i * subnet_step
        for j in range(3, -1, -1):
            while subnet_start[j] > 255:
                subnet_start[j] -= 256
                if j > 0:
                    subnet_start[j-1] += 1
        subnet_network = ".".join(map(str, subnet_start))
        subnet_broadcast = calculate_network_broadcast(subnet_network, cidr)[1]
        subnet_first_usable, subnet_last_usable = usable_ip_range(subnet_network, subnet_broadcast)
        subnets.append({
            "network": subnet_network,
            "broadcast": subnet_broadcast,
            "range": (subnet_first_usable, subnet_last_usable)
        })
    return subnets

def display_summary(ip, cidr, subnet_mask, details, parent_cidr):
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}IPv4 SUBNET CALCULATOR")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.WHITE}• IP Address: {Fore.GREEN}{ip}")
    print(f"{Fore.WHITE}• Network Address: {Fore.GREEN}{details['network']}")
    print(f"{Fore.WHITE}• Usable Host IP Range: {Fore.GREEN}{details['range'][0]} - {details['range'][1]}")
    print(f"{Fore.WHITE}• Broadcast Address: {Fore.GREEN}{details['broadcast']}")
    print(f"{Fore.WHITE}• Total Number of Hosts: {Fore.GREEN}{details['possible']}")
    print(f"{Fore.WHITE}• Number of Usable Hosts: {Fore.GREEN}{details['usable']}")
    print(f"{Fore.WHITE}• Subnet Mask: {Fore.GREEN}{details['subnet_mask']}")
    print(f"{Fore.WHITE}• Subnet Location: {Fore.GREEN}Subnet {details['subnet_location']} of {details['num_subnets']} subnets")
    print(f"{Fore.WHITE}• Wildcard Mask: {Fore.GREEN}{details['wildcard_mask']}")
    print(f"{Fore.WHITE}• Binary Subnet Mask: {Fore.GREEN}{details['binary']}")
    print(f"{Fore.WHITE}• IP Class: {Fore.GREEN}{details['ip_class']}")
    print(f"{Fore.WHITE}• CIDR Notation: {Fore.GREEN}/{cidr}")
    print(f"{Fore.WHITE}• IP Type: {Fore.GREEN}{details['ip_type']}")
    print(f"{Fore.WHITE}• Binary ID: {Fore.GREEN}{details['ip_binary']}")
    print(f"{Fore.WHITE}• Integer ID: {Fore.GREEN}{details['integer_id']}")
    print(f"{Fore.WHITE}• Hex ID: {Fore.GREEN}{details['hex_id']}")
    print(f"{Fore.WHITE}• in-addr.arpa: {Fore.GREEN}{details['in_addr_arpa']}")
    
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}All Possible /{cidr} Networks for {details['parent_network']}")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.GREEN + Style.BRIGHT}{'Network Address':<20} {'Usable Host Range':<30} {'Broadcast Address':<20} {'Suggested Gateway':<20}")
    for i, subnet in enumerate(generate_subnets(details['parent_network'], parent_cidr, cidr, details['num_subnets']), 1):
        print(f"{Fore.WHITE}└─ Subnet {i}:")
        print(f"{Fore.WHITE}   ├─ Network: {Fore.GREEN}{subnet['network']:<20}")
        print(f"{Fore.WHITE}   ├─ Usable Range: {Fore.GREEN}{subnet['range'][0]} - {subnet['range'][1]:<30}")
        print(f"{Fore.WHITE}   ├─ Broadcast: {Fore.GREEN}{subnet['broadcast']:<20}")
        print(f"{Fore.WHITE}   └─ Gateway: {Fore.GREEN}{subnet['range'][0]:<20}")
    
    print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    print(f"{Fore.CYAN + Style.BRIGHT}Computation Options:")
    print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
    options = [
        "Assigned Usable IP Address",
        "Solution For IP Binary Notation",
        "Solution for Subnet/CIDR Binary Notation",
        "Solution for First IP Address (Network Address)",
        "Solution for Last IP Address (Broadcast Address)",
        "Solution for Total Number of Subnets",
        "Solution for Number of Possible Addresses",
        "Solution for Total Number of Usable Addresses",
        "Solution for Subnet Steps",
        "Solution for the Location of the IP Address on what Subnet",
        "End the program"
    ]
    for i, opt in enumerate(options, 1):
        print(f"{Fore.WHITE}• {i}. {opt}")

def main():
    print_header()
    while True:
        print(f"{Fore.BLUE + Style.BRIGHT}➤ Please Enter the IP Address:")
        try:
            ip = input(f"{Fore.BLUE}> ")
        except EOFError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
            return
        try:
            octets = ip.split('.')
            if len(octets) == 4 and all(0 <= int(octet) <= 255 for octet in octets):
                special_type = is_special_ip(ip)
                if special_type:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Warning: {ip} is a {special_type} address. Proceeding for educational purposes.")
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Invalid IP address. Enter four octets between 0 and 255.")
        except ValueError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Invalid IP address. Use dotted decimal format (e.g., 192.168.1.0).")
    
    while True:
        print(f"\n{Fore.BLUE + Style.BRIGHT}Select the Parent Network CIDR/Subnet")
        print(f"{Fore.WHITE}1. Class A (/8 or 255.0.0.0)")
        print(f"{Fore.WHITE}2. Class B (/16 or 255.255.0.0)")
        print(f"{Fore.WHITE}3. Class C (/24 or 255.255.255.0)")
        print(f"{Fore.WHITE}4. Class D (/32 or 255.255.255.255)")
        print(f"{Fore.BLUE + Style.BRIGHT}➤ Enter your choice (1-4):")
        try:
            choice = input(f"{Fore.BLUE}> ")
            if choice in ["1", "2", "3", "4"]:
                parent_cidr = {"1": 8, "2": 16, "3": 24, "4": 32}[choice]
                break
            print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Please select 1, 2, 3, or 4.")
        except EOFError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
            return
    
    while True:
        print(f"\n{Fore.BLUE + Style.BRIGHT}➤ What type? Subnet (1) or CIDR (2):")
        try:
            choice = input(f"{Fore.BLUE}> ")
        except EOFError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
            return
        if choice in ["1", "2"]:
            break
        print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Enter 1 for Subnet or 2 for CIDR.")
    
    if choice == "1":
        while True:
            print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Enter the Subnet:")
            try:
                subnet_mask = input(f"{Fore.BLUE}> ")
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
            try:
                octets = subnet_mask.split('.')
                if len(octets) != 4 or not all(0 <= int(octet) <= 255 for octet in octets):
                    print(f"{Fore.RED + Style.BRIGHT}✖ Invalid subnet mask. Please enter a valid subnet mask (e.g., 255.255.255.0)")
                    continue
                cidr = mask_to_cidr(subnet_mask)
                if cidr < parent_cidr:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Subnet CIDR (/{cidr}) must be greater than or equal to parent CIDR (/{parent_cidr}).")
                    continue
                break
            except ValueError as e:
                print(f"{Fore.RED + Style.BRIGHT}✖ Error: {e}")
    else:
        while True:
            print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Enter the CIDR: /")
            try:
                cidr = input(f"{Fore.BLUE}> ")
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
            try:
                cidr = int(cidr)
                if 0 <= cidr <= 32 and cidr >= parent_cidr:
                    subnet_mask = cidr_to_mask(cidr)
                    break
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid CIDR. Enter a value between {parent_cidr} and 32.")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid input. Enter a numeric CIDR value.")
    
    details = subnet_details(ip, parent_cidr, cidr)
    display_summary(ip, cidr, subnet_mask, details, parent_cidr)
    
    while True:
        print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Select an option:")
        try:
            choice = input(f"{Fore.BLUE}> ")
        except EOFError:
            print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
            return
        
        if choice == "1":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}ASSIGNED USABLE IP ADDRESS")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.BLUE + Style.BRIGHT}➤ Please specify how many devices per subnet:")
            try:
                num_devices = input(f"{Fore.BLUE}> ")
                num_devices = int(num_devices)
                if num_devices <= 0:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Enter a positive number of devices.")
                    continue
                print(f"{Fore.BLUE + Style.BRIGHT}➤ Randomized (1) or Sequence (2):")
                mode = input(f"{Fore.BLUE}> ")
                if mode not in ["1", "2"]:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Enter 1 for Randomized or 2 for Sequence.")
                    continue
                
                subnets = generate_subnets(details['parent_network'], details['parent_cidr'], cidr, details['num_subnets'])
                for i, subnet in enumerate(subnets, 1):
                    first_usable, last_usable = subnet['range']
                    max_usable = details['usable']
                    try:
                        ips = generate_usable_ips(first_usable, last_usable, num_devices, mode, max_usable)
                        print(f"\n{Fore.WHITE}└─ Subnet {i}: {Fore.GREEN}{subnet['network']}/{cidr}")
                        print(f"{Fore.WHITE}   ├─ Network Address: {Fore.GREEN}{subnet['network']}")
                        print(f"{Fore.WHITE}   ├─ Broadcast Address: {Fore.GREEN}{subnet['broadcast']}")
                        print(f"{Fore.WHITE}   ├─ Usable IP Range: {Fore.GREEN}{first_usable} - {last_usable}")
                        print(f"{Fore.WHITE}   └─ Assigned IPs:")
                        for j, ip_addr in enumerate(ips, 1):
                            print(f"{Fore.WHITE}      └─ IP {chr(64 + j)}: {Fore.GREEN}{ip_addr}")
                    except ValueError as e:
                        print(f"{Fore.RED + Style.BRIGHT}✖ Error for Subnet {i}: {e}")
                try:
                    print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                    input(f"{Fore.BLUE}> ")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    display_summary(ip, cidr, subnet_mask, details, parent_cidr)
                except EOFError:
                    print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                    return
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid input. Enter a positive integer for the number of devices.")
        
        elif choice == "2":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}IP BINARY NOTATION")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.GREEN}IP Address: {ip}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE + Style.BRIGHT}Step 1: Convert each octet to 8-bit binary")
            ip_octets = ip.split(".")
            binary_parts = []
            for i, octet in enumerate(ip_octets, 1):
                octet = int(octet)
                binary = bin(octet)[2:].zfill(8)
                powers = [128, 64, 32, 16, 8, 4, 2, 1]
                breakdown = [str(p) for p, b in zip(powers, binary) if b == '1']
                breakdown_str = " + ".join(breakdown) if breakdown else "0"
                print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{octet} = {breakdown_str} = {binary}")
                binary_parts.append(binary)
            binary = ".".join(binary_parts)
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ {binary}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "3":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}SUBNET/CIDR BINARY NOTATION")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.GREEN}Subnet Mask: {subnet_mask}")
            print(f"{Fore.GREEN}CIDR: /{cidr}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE + Style.BRIGHT}Step 1: Convert each octet to 8-bit binary")
            mask_octets = subnet_mask.split(".")
            binary_parts = []
            for i, octet in enumerate(mask_octets, 1):
                octet = int(octet)
                binary = bin(octet)[2:].zfill(8)
                powers = [128, 64, 32, 16, 8, 4, 2, 1]
                breakdown = [str(p) for p, b in zip(powers, binary) if b == '1']
                breakdown_str = " + ".join(breakdown) if breakdown else "0"
                print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{octet} = {breakdown_str} = {binary}")
                binary_parts.append(binary)
            binary = ".".join(binary_parts)
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ {binary}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "4":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}FIRST IP ADDRESS (NETWORK ADDRESS)")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.BLUE + Style.BRIGHT}➤ What method?")
            print(f"{Fore.WHITE}• 1. Long Method")
            print(f"{Fore.WHITE}• 2. Short Method")
            try:
                method_choice = input(f"{Fore.BLUE}> ")
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
            if method_choice == "1":
                long_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            elif method_choice == "2":
                short_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            else:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Enter 1 or 2.")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "5":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}LAST IP ADDRESS (BROADCAST ADDRESS)")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.BLUE + Style.BRIGHT}➤ What method?")
            print(f"{Fore.WHITE}• 1. Long Method")
            print(f"{Fore.WHITE}• 2. Short Method")
            try:
                method_choice = input(f"{Fore.BLUE}> ")
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
            if method_choice == "1":
                long_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            elif method_choice == "2":
                short_method(ip, subnet_mask, cidr, details['network'], details['broadcast'])
            else:
                print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Enter 1 or 2.")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "6":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}TOTAL NUMBER OF SUBNETS")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE}└─ Parent CIDR: {Fore.GREEN}/{details['parent_cidr']}")
            print(f"{Fore.WHITE}└─ Subnet CIDR: {Fore.GREEN}/{cidr}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 1: Calculate borrowed bits (m)")
            borrowed_bits = cidr - details['parent_cidr']
            print(f"{Fore.WHITE}└─ m = {Fore.GREEN}{cidr} - {details['parent_cidr']} = {borrowed_bits}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 2: Calculate total subnets (2^m)")
            total_subnets = 2 ** borrowed_bits
            print(f"{Fore.WHITE}└─ 2^{borrowed_bits} = {Fore.GREEN}{total_subnets}")
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ Total Number of Subnets = {details['num_subnets']}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "7":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}NUMBER OF POSSIBLE ADDRESSES")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE}└─ CIDR: {Fore.GREEN}/{cidr}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 1: Calculate host bits (n)")
            host_bits = 32 - cidr
            print(f"{Fore.WHITE}└─ n = {Fore.GREEN}32 - {cidr} = {host_bits}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 2: Calculate total possible addresses (2^n)")
            total_addresses = 2 ** host_bits
            print(f"{Fore.WHITE}└─ 2^{host_bits} = {Fore.GREEN}{total_addresses}")
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ Number of Possible Addresses = {details['possible']}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "8":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}TOTAL NUMBER OF USABLE ADDRESSES")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE}└─ CIDR: {Fore.GREEN}/{cidr}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 1: Calculate total possible addresses")
            host_bits = 32 - cidr
            total_addresses = 2 ** host_bits
            print(f"{Fore.WHITE}└─ Host bits (n) = {Fore.GREEN}32 - {cidr} = {host_bits}")
            print(f"{Fore.WHITE}└─ Total addresses = 2^{host_bits} = {Fore.GREEN}{total_addresses}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 2: Subtract network and broadcast addresses")
            usable_addresses = total_addresses - 2
            print(f"{Fore.WHITE}└─ {total_addresses} - 2 = {Fore.GREEN}{usable_addresses}")
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ Total Number of Usable Addresses = {details['usable']}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "9":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}SUBNET STEPS")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE}└─ CIDR: {Fore.GREEN}/{cidr}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 1: Calculate host bits (n)")
            host_bits = 32 - cidr
            print(f"{Fore.WHITE}└─ n = {Fore.GREEN}32 - {cidr} = {host_bits}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 2: Calculate subnet step (2^n)")
            subnet_step = 2 ** host_bits
            print(f"{Fore.WHITE}└─ 2^{host_bits} = {Fore.GREEN}{subnet_step}")
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ Subnet Step = {details['subnet_step']}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "10":
            print(f"\n{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.CYAN + Style.BRIGHT}LOCATION OF THE IP ADDRESS ON WHAT SUBNET")
            print(f"{Fore.YELLOW + Style.BRIGHT}{'─'*50}")
            print(f"{Fore.WHITE + Style.BRIGHT}Solution:")
            print(f"{Fore.WHITE}└─ IP Address: {Fore.GREEN}{ip}")
            print(f"{Fore.WHITE}└─ Parent Network: {Fore.GREEN}{details['parent_network']}/{details['parent_cidr']}")
            print(f"{Fore.WHITE}└─ Subnet CIDR: {Fore.GREEN}/{cidr}")
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 1: Find the Network Address using IP AND Subnet Mask")
            ip_octets = [int(o) for o in ip.split(".")]
            mask_octets = [int(o) for o in subnet_mask.split(".")]
            network = [ip_octets[i] & mask_octets[i] for i in range(4)]
            network_str = ".".join(map(str, network))
            for i, (ip_octet, mask_octet, net_octet) in enumerate(zip(ip_octets, mask_octets, network), 1):
                ip_bin = bin(ip_octet)[2:].zfill(8)
                mask_bin = bin(mask_octet)[2:].zfill(8)
                net_bin = bin(net_octet)[2:].zfill(8)
                print(f"{Fore.WHITE}├─ Octet {i}: {Fore.GREEN}{ip_octet} ({ip_bin}) {Fore.WHITE}AND {Fore.GREEN}{mask_octet} ({mask_bin}) {Fore.WHITE}= {Fore.GREEN}{net_octet} ({net_bin})")
            print(f"\n{Fore.WHITE}└─ Network Address: {Fore.GREEN}{network_str}")
            
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 2: Identify the Affected Octet")
            borrowed_bits = cidr - details['parent_cidr']
            parent_mask = cidr_to_mask(details['parent_cidr'])
            parent_octets = [int(o) for o in parent_mask.split(".")]
            subnet_octets = [int(o) for o in subnet_mask.split(".")]
            affected_octet_idx = next(i for i in range(4) if parent_octets[i] != subnet_octets[i])
            print(f"{Fore.WHITE}├─ Parent CIDR: {Fore.GREEN}/{details['parent_cidr']} ({parent_mask})")
            print(f"{Fore.WHITE}├─ Subnet CIDR: {Fore.GREEN}/{cidr} ({subnet_mask})")
            print(f"{Fore.WHITE}├─ Borrowed bits: {Fore.GREEN}{borrowed_bits}")
            print(f"{Fore.WHITE}└─ Affected Octet: {Fore.GREEN}{affected_octet_idx + 1}th octet")
            
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 3: Calculate the Increment")
            bits_in_affected = bin(subnet_octets[affected_octet_idx])[2:].count("1") - bin(parent_octets[affected_octet_idx])[2:].count("1")
            increment = 2 ** (8 - bits_in_affected)
            print(f"{Fore.WHITE}├─ Borrowed bits in affected octet: {Fore.GREEN}{bits_in_affected}")
            print(f"{Fore.WHITE}└─ Increment = {Fore.GREEN}2^(8 - {bits_in_affected}) = {increment}")
            
            print(f"\n{Fore.WHITE + Style.BRIGHT}Step 4: Calculate Subnet Location")
            affected_value = network[affected_octet_idx]
            location = (affected_value // increment) + 1
            print(f"{Fore.WHITE}├─ Network Address: {Fore.GREEN}{network_str}")
            print(f"{Fore.WHITE}├─ Affected Octet Value: {Fore.GREEN}{affected_value}")
            print(f"{Fore.WHITE}└─ Location = {Fore.GREEN}({affected_value} ÷ {increment}) + 1 = {location}")
            
            print(f"\n{Fore.WHITE}└─ Result: {Fore.MAGENTA}✔ Subnet {details['subnet_location']} of {details['num_subnets']} subnets")
            print(f"{Fore.WHITE}   ├─ Network Address: {Fore.GREEN}{details['network']}")
            print(f"{Fore.WHITE}   ├─ Usable Host Range: {Fore.GREEN}{details['range'][0]} - {details['range'][1]}")
            print(f"{Fore.WHITE}   └─ Broadcast Address: {Fore.GREEN}{details['broadcast']}")
            try:
                print(f"\n{Fore.BLUE + Style.BRIGHT}➤ Press Enter key to return to the Network Summary")
                input(f"{Fore.BLUE}> ")
                os.system('cls' if os.name == 'nt' else 'clear')
                display_summary(ip, cidr, subnet_mask, details, parent_cidr)
            except EOFError:
                print(f"{Fore.RED + Style.BRIGHT}✖ Input stream closed. Exiting program.")
                return
        
        elif choice == "11":
            print(f"{Fore.CYAN + Style.BRIGHT}Program ended.")
            break
        else:
            print(f"{Fore.RED + Style.BRIGHT}✖ Invalid choice. Enter a number between 1 and 11.")

if __name__ == "__main__":
    main()