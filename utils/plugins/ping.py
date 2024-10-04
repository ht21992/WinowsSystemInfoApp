import os
import socket
import struct
import select
import time
import random

# Timer function to measure the time
default_timer = time.time

# ICMP type for Echo Request
ICMP_ECHO_REQUEST = 8


def checksum(source_string):
    """
    
    Calculate the checksum of the packet header and data for error-checking in ICMP protocol.

    The Internet Control Message Protocol (ICMP): a network layer protocol used by network devices to diagnose
    network communication issues

    """
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xFFFFFFFF
        count += 2

    if count_to < len(source_string):
        sum += source_string[-1]
        sum = sum & 0xFFFFFFFF

    sum = (sum >> 16) + (sum & 0xFFFF)
    sum += sum >> 16
    answer = ~sum
    answer = answer & 0xFFFF
    answer = answer >> 8 | (answer << 8 & 0xFF00)

    return answer


def receive_one_ping(sock, packet_id, timeout):
    """
    Wait for the response (Echo Reply) to the sent ICMP Echo Request.
    It reads the packet and checks if the ID matches the one we sent.
    """
    time_left = timeout
    while True:
        start_time = default_timer()
        ready = select.select([sock], [], [], time_left)
        time_spent = default_timer() - start_time

        if ready[0] == []:  # Timeout
            return None

        time_received = default_timer()
        rec_packet, addr = sock.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, received_id, sequence = struct.unpack(
            "bbHHh", icmp_header
        )

        if type == 0 and received_id == packet_id:  # Echo Reply and packet ID matches
            data_size = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28 : 28 + data_size])[0]
            return time_received - time_sent

        time_left -= time_spent
        if time_left <= 0:
            return None


def send_one_ping(sock, dest_addr, packet_id):
    """
    Send an ICMP Echo Request to the destination address with a unique packet ID.
    """
    dest_addr = socket.gethostbyname(dest_addr)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, packet_id, 1)
    data = struct.pack("d", default_timer()) + (192 - struct.calcsize("d")) * b"Q"

    # Calculate the checksum
    my_checksum = checksum(header + data)
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), packet_id, 1
    )
    packet = header + data

    sock.sendto(packet, (dest_addr, 1))


def ping(dest_addr, timeout=2):
    """
    Ping a host on the network by sending an ICMP Echo Request and waiting for an Echo Reply.

    Args:
        dest_addr (str): The destination IP address or hostname to ping.
        timeout (int): The maximum time (in seconds) to wait for a response.

    Returns:
        float: The round-trip delay time in seconds if successful, or:
               -3 if there is an error creating the socket,
               -2 if there is an error sending the ping,
               -1 if the request times out.
    """
    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError:
        return -3

    packet_id = random.randint(1, 65535) & 0xFFFF

    try:
        send_one_ping(sock, dest_addr, packet_id)
        delay = receive_one_ping(sock, packet_id, timeout)
    except Exception:
        return -2

    sock.close()
    if delay is None:
        return -1
    return delay


if __name__ == "__main__":
    pass
    # from tools import radar

    # print(radar())
