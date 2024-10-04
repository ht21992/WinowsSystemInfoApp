import psutil
import socket

"""
Netstat Displays active TCP connections, ports on which the computer is listening,
Ethernet statistics, the IP routing table, IPv4 statistics (for the IP, ICMP, TCP, and UDP protocols),
and IPv6 statistics (for the IPv6, ICMPv6, TCP over IPv6, and UDP over IPv6 protocols)
"""

# Mapping of TCP states to their human-readable names
TCP_STATES = {
    "01": "ESTABLISHED",
    "02": "SYN_SENT",
    "03": "SYN_RECV",
    "04": "FIN_WAIT1",
    "05": "FIN_WAIT2",
    "06": "TIME_WAIT",
    "07": "CLOSE",
    "08": "CLOSE_WAIT",
    "09": "LAST_ACK",
    "0A": "LISTEN",
    "0B": "CLOSING",
}


class NetstatWindows:
    def _get_tcp_connections(self):
        """
        Use psutil to retrieve the list of TCP connections on a Windows system.
        """
        return psutil.net_connections(kind="tcp")

    def _ip_port_from_tuple(self, address):
        """
        Convert IP and port from psutil tuple to a more readable format.
        """
        ip, port = address
        return ip, port

    def get_netstat(self):
        """
        Retrieve TCP connection details for Windows systems using psutil.
        Returns a list of dictionaries with connection info.
        """
        tcp_connections = self._get_tcp_connections()
        result = []
        for conn in tcp_connections:
            # Retrieve local and remote addresses (if available)
            l_host, l_port = self._ip_port_from_tuple(conn.laddr)
            r_host, r_port = (
                self._ip_port_from_tuple(conn.raddr) if conn.raddr else ("", 0)
            )

            # Get connection state (already in human-readable format from psutil)
            state = conn.status

            # Get process ID and executable name
            pid = conn.pid
            try:
                process = psutil.Process(pid)
                exe = process.exe()  # Get the executable for the process
                user = process.username()  # Get the user running the process
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                exe = None
                user = None

            # Get service name from local port (if available)
            try:
                service = socket.getservbyport(l_port)
            except:
                service = None

            connection_info = {
                "pid": pid,
                "uid": user,
                "service": service,
                "local_port": l_port,
                "local_address": l_host,
                "remote_port": r_port,
                "remote_address": r_host,
                "state": state,
                "executable": exe,
            }
            result.append(connection_info)
        return result


if __name__ == "__main__":
    pass
    # net_stat = NetstatWindows()
    # print(net_stat.get_netstat())
