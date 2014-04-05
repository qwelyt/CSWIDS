from wifi_scan_linux.ifiw import ifiw

def scan(interface):
    ''' Returns all found access points '''
    aps = ifiw.ifiw.scan(interface)
    return aps

def traceroute(dest, hops=30):
    ''' Returns a dict with all the hops that were made to reach the destination.

        dest -- The destination to reach
        hops -- The maximum number of hops to perform.
    '''
    dest_addr = socket.gethostbyname(dest)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    port = 33434
    max_hops = hops
    data = ""
    data = data.encode('utf-8')
    route = {}
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        recv_socket.bind(("", port))
        send_socket.sendto(data, (dest, port))

        curr_addr = None
        curr_name = None
        try:
            _, curr_addr = recv_socket.recvfrom(1024)
            curr_addr = curr_addr[0]
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr
        except socket.error:
            pass
        finally:
            recv_socket.close()
            send_socket.close()

        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = "*"
        route[ttl] = curr_host


        ttl += 1

        if curr_addr == dest_addr or ttl > max_hops:
            return route

def test_ap_linux(interface, ap1, ap2):
    ''' Returns "Safe", "Unsafe", or "Unknown" '''
    # Should perform the tests needed.
    # 1. Connect to ap and check it's ip, essid, bssid.
    # 2. Compare to other aps results.
    # 3. If they are the same:
    #       Traceroute to some dest from both APs
    #       if traceroute is the same:
    #           N/A
    #       else:
    #           Unknown
    #    else:
    #       if netID is the same:
    #           Safe
    #       else:
    #           Traceroute some dest from both APs
    #           if traceroute is the same:
    #               Unknown
    #           else: (if there is an extra hop)
    #               Unsafe
    
    # Connect and traceroute AP1


    return "Unknown"
