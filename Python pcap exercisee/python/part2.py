import struct
import argparse

def read_pcap(file_path):
    with open(file_path, 'rb') as file:
        file.read(24)  # Skip the global pcap header 24 bytes
        packets = []
        while True:
            # Read packet header 
            packet_header = file.read(16)
            if len(packet_header) < 16:
                break  
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('=IIII', packet_header)
            packet = file.read(incl_len)  # Read packet data based on included length
            packets.append((ts_sec, ts_usec, packet))  # Store as a tuple
        return packets

def extract_ip_header(packet):
    # Extracts the IP header from a packet and returns source IP, destination IP and protocol
    if len(packet) >= 34:  # Ensure packet is large enough
        ip_header = packet[14:34]  # Extract the IP header 
        ip_fields = struct.unpack('!BBHHHBBH4s4s', ip_header)  # Unpack IP header
        source_ip = '.'.join(map(str, ip_fields[8]))  # Convert source IP to format
        dest_ip = '.'.join(map(str, ip_fields[9]))  
        protocol = ip_fields[6]  # Extract protocol field
        return source_ip, dest_ip, protocol
    return None, None, None  # Return None if packet is too short

def extract_ports(packet, protocol):
    # Extracts source and destination ports if the packet is TCP or UDP
    if protocol == 6 and len(packet) >= 54:  
        tcp_header = packet[34:54]  
        tcp_fields = struct.unpack('!HHLLBBHHH', tcp_header)  # Unpack TCP header fields
        return tcp_fields[0], tcp_fields[1]  # Return source + destination ports
    elif protocol == 17 and len(packet) >= 42:  # Check for UDP protocol + ensure packet size
        udp_header = packet[34:42]  # Extract UDP header
        udp_fields = struct.unpack('!HHHH', udp_header)  
        return udp_fields[0], udp_fields[1]  
    return None, None  # Return None if issue

def cluster_by_time_or_port(packets, target_ip, width, min_packets, mode='time'):
    # Groups packets into clusters on time for probing or port for scanning
    clusters = []
    # Sort packets on time or destination port
    packets.sort(key=lambda x: (x[0], x[1]) if mode == 'time' else extract_ports(x[2], extract_ip_header(x[2])[2])[1] or 0)
    
    current_cluster = None  
    for ts_sec, ts_usec, packet in packets:
        source_ip, dest_ip, protocol = extract_ip_header(packet)
        if dest_ip != target_ip:
            continue  # Skip packets that do not have the target IP as the destination
        source_port, dest_port = extract_ports(packet, protocol)
        if source_port is None or dest_port is None:
            continue  # Skip packets without valid source/destination ports

        key_value = ts_sec if mode == 'time' else dest_port  # Determine key value based on mode
        cluster_key = 'start_time' if mode == 'time' else 'start_port'  # Cluster key

        if not current_cluster:
            # Start a new cluster
            current_cluster = {cluster_key: key_value, 'count': 1, 'sources': {source_ip}}
        elif abs(key_value - current_cluster[cluster_key]) <= width:
            # Add to the current cluster if yes
            current_cluster['count'] += 1
            current_cluster['sources'].add(source_ip)
        else:
            # Finish the current cluster and start a new one
            if current_cluster['count'] >= min_packets:
                clusters.append(current_cluster)
            current_cluster = {cluster_key: key_value, 'count': 1, 'sources': {source_ip}}

    # Add the last cluster if it meets the minimum packet count
    if current_cluster and current_cluster['count'] >= min_packets:
        clusters.append(current_cluster)

    return clusters

def identify_clusters(packets, target_ip, wp, np, ws, ns):
    # Separates TCP and UDP packets and creates probing and scanning clusters
    tcp_packets = [pkt for pkt in packets if extract_ip_header(pkt[2])[2] == 6]  # TCP packets
    udp_packets = [pkt for pkt in packets if extract_ip_header(pkt[2])[2] == 17]  # UDP packets

    # Create probing clusters and scanning clusters
    probing_clusters_tcp = cluster_by_time_or_port(tcp_packets, target_ip, wp, np, mode='time')
    probing_clusters_udp = cluster_by_time_or_port(udp_packets, target_ip, wp, np, mode='time')
    scanning_clusters_tcp = cluster_by_time_or_port(tcp_packets, target_ip, ws, ns, mode='port')
    scanning_clusters_udp = cluster_by_time_or_port(udp_packets, target_ip, ws, ns, mode='port')

    return probing_clusters_tcp, scanning_clusters_tcp, probing_clusters_udp, scanning_clusters_udp

def main():
    parser = argparse.ArgumentParser(description="Detect probing and scanning in PCAP files.")
    parser.add_argument('-f', '--file', required=True, help="PCAP file path.")
    parser.add_argument('-t', '--target', required=True, help="Target IP address.")
    parser.add_argument('-l', '--wp', type=float, required=True, help="Width for probing (seconds).")
    parser.add_argument('-m', '--np', type=int, required=True, help="Minimum packets for probing.")
    parser.add_argument('-n', '--ws', type=int, required=True, help="Width for scanning (port numbers).")
    parser.add_argument('-p', '--ns', type=int, required=True, help="Minimum packets for scanning.")
    args = parser.parse_args()

    packets = read_pcap(args.file)  
    probing_clusters_tcp, scanning_clusters_tcp, probing_clusters_udp, scanning_clusters_udp = identify_clusters(
        packets, args.target, args.wp, args.np, args.ws, args.ns)

    with open('part2_output.txt', 'a') as output_file:
        output_file.write(f"\n\n{'=' * 10} File: {args.file} {'=' * 10}\n")
        output_file.write(f"{'-' * 10} Args: -t {args.target} -l {args.wp} -m {args.np} -n {args.ws} -p {args.ns} {'-' * 10}\n")

        def output_clusters(protocol, probing_clusters, scanning_clusters):
            # Writes clusters to the output file
            probing_index = 1
            scanning_index = 1

            if probing_clusters:
                output_file.write(f"\n\n{'*' * 4} {protocol} Probe Clusters {'*' * 4}\n\n")
                for cluster in probing_clusters:
                    output_file.write(f"{protocol} Probe Nb: {probing_index}:\n")
                    output_file.write(f"Source IP: {', '.join(cluster['sources'])}\n")
                    output_file.write(f"Nb Packets: {cluster['count']}\n\n")
                    probing_index += 1

            if scanning_clusters:
                output_file.write(f"\n\n{'*' * 4} {protocol} Scan Clusters {'*' * 4}\n\n")
                for cluster in scanning_clusters:
                    output_file.write(f"{protocol} Scan Nb: {scanning_index}:\n")
                    output_file.write(f"Source IP: {', '.join(cluster['sources'])}\n")
                    output_file.write(f"Nb Packets: {cluster['count']}\n\n")
                    scanning_index += 1

        output_clusters('TCP', probing_clusters_tcp, scanning_clusters_tcp)
        output_clusters('UDP', probing_clusters_udp, scanning_clusters_udp)

if __name__ == '__main__':
    main()
