import os
import struct
import socket

def read_pcap(file_path):
    # Opens the pcap file and reads packet data
    with open(file_path, 'rb') as f:
        f.read(24)  # Skip the global header (24 bytes) of the pcap file
        packets = []
        while True:
            packet_header = f.read(16)  # Read the packet header (16 bytes)
            if len(packet_header) < 16:
                break  
            packet_length = struct.unpack('I', packet_header[8:12])[0]  # Extract packet length
            packet_data = f.read(packet_length)  
            packets.append(packet_data)  
        return packets

def extract_ip_and_ports(packet):
    # Extracts source IP, destination TCP port and source IP-destination port pair
    eth_header = struct.unpack('!6s6sH', packet[:14])  # Unpack Ethernet header first 14 bytes
    if eth_header[2] != 0x0800:  # Check if the packet IPv4
        return None, None, None  # Return None if not

    ip_header = packet[14:34]  # Extract the IP header 
    ip_header_unpacked = struct.unpack('!BBHHHBBH4s4s', ip_header) 
    protocol = ip_header_unpacked[6]  # Extract protocol field 6th byte of IP header
    if protocol != 6:  # Check if TCP 6
        return None, None, None  # Return None if not

    source_ip = socket.inet_ntoa(ip_header_unpacked[8])  # Convert source IP to readable format
    destination_ip = socket.inet_ntoa(ip_header_unpacked[9]) 
    tcp_header = packet[34:54]  # Extract the TCP header 
    source_port, dest_port = struct.unpack('!HH', tcp_header[:4])  # Extract source and destination ports
    return source_ip, dest_port, (source_ip, dest_port)  # Return source IP, destination port and IP port pair

def analyze_single_pcap(file):
    
    packets = read_pcap(file)  
    total_packet_count = len(packets)  # Count total packets in the file
    source_ip_count = {}  # Dictionary
    dest_port_count = {}  
    src_ip_dest_port_pairs = {}  

    for packet in packets:
        source_ip, dest_port, src_ip_dest_port_pair = extract_ip_and_ports(packet)
        if source_ip:
            # Increment count of packets for the source IP
            source_ip_count[source_ip] = source_ip_count.get(source_ip, 0) + 1
        if dest_port:
            
            dest_port_count[dest_port] = dest_port_count.get(dest_port, 0) + 1
        if src_ip_dest_port_pair:
            
            src_ip_dest_port_pairs[src_ip_dest_port_pair] = src_ip_dest_port_pairs.get(src_ip_dest_port_pair, 0) + 1

    return total_packet_count, source_ip_count, dest_port_count, src_ip_dest_port_pairs

def format_and_write_results(file, total_packet_count, source_ip_count, dest_port_count, src_ip_dest_port_pairs, output_file):
    
    with open(output_file, 'a') as f:
        f.write(f"Results for {file}:\n\n")
        f.write(f"Total number of packets: {total_packet_count}\n\n")

        
        f.write("Distinct Source IP Addresses:\n")
        for ip, count in sorted(source_ip_count.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{ip}: {count} packets\n")
        f.write("\n")

        
        f.write("Distinct Destination TCP Ports:\n")
        for port, count in sorted(dest_port_count.items(), key=lambda x: x[1], reverse=True):
            f.write(f"Port {port}: {count} packets\n")
        f.write("\n")

        
        f.write("Distinct Source IP and Destination TCP Port Pairs:\n")
        for pair, count in sorted(src_ip_dest_port_pairs.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{pair[0]} -> Port {pair[1]}: {count} packets\n")
        f.write("\n" + "="*45 + "\n\n")

if __name__ == "__main__":
    
    pcap_files = ['file1.pcap', 'file2.pcap', 'file3.pcap']  

    
    output_file = "part1_output.txt"
    open(output_file, 'w').close()  

    total_packets_all_files = 0  # Variable to accumulate the total packet count across all files

    # Analyze each pcap file
    for file in pcap_files:
        total_count, source_ips, dest_ports, src_ip_dest_pairs = analyze_single_pcap(file)
        total_packets_all_files += total_count  # Update the total packet count
        format_and_write_results(file, total_count, source_ips, dest_ports, src_ip_dest_pairs, output_file)

    # Write the total number of packets for all files at the beginning
    with open(output_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f"Total number of packets across all files: {total_packets_all_files}\n\n" + content)
