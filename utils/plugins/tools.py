import socket
import psutil
from ping import ping
import netaddr
from multiprocessing.pool import ThreadPool
from time import sleep


def convert_to_gb(val: int):
    return round(val / 1e9, 2)


def get_primary_ip() -> str:
    ips = socket.gethostbyname_ex(socket.gethostname())[2]
    ips = [ip for ip in ips if not ip.startswith("127.")]

    if len(ips) > 0:
        return ips[0]

    return ""


def radar() -> list:
    """
    Scans the local network by pinging all available IP addresses in the same subnet as the machine's primary IP.

    It identifies the network interface, determines the subnet based on the IP address and netmask, and then pings each host in the network to measure response times.
    A thread pool is used to ping multiple addresses concurrently. The function returns a list of IP addresses that responded to the ping with a positive delay.

    Returns:
        list: A list of tuples containing the IP addresses and their respective ping delays for hosts that responded.
    """
    addresses = psutil.net_if_addrs()

    def lping(address, timeout):
        delay = ping(str(address), timeout=0.5)
        return (address, delay)

    ip = get_primary_ip()
    for device in addresses.keys():
        for address in addresses[device]:
            if address.address == ip:
                netmask = address.netmask

    network = ip + "/" + str(netaddr.IPAddress(netmask).netmask_bits())
    address_list = list(netaddr.IPNetwork(network).iter_hosts())
    ping_results = []

    pool = ThreadPool(processes=1000)
    async_results = []
    for address in address_list:
        async_results.append(pool.apply_async(lping, (str(address), 0.5)))

    sleep(1)

    for asyng_result in async_results:
        ping_results.append(asyng_result.get())

    return [ping for ping in ping_results if ping[1] > 0]
