import socket
import os
from time import sleep
from wifi_scan_linux.ifiw import ifiw


def scan(interface):
    ''' Returns all found access points '''
    aps = ifiw.ifiw.scan(interface)
    return aps

def traceroute(dest, interface, hops=30):
    ''' Returns a dict with all the hops that were made to reach the destination.

        dest -- The destination to reach
        hops -- The maximum number of hops to perform.
    '''
    print(dest + " <-- traceroute")
    dest_addr = ""
    tries = 1
    while dest_addr == "":
        print("Try number: "+ str(tries))
        try:
            dest_addr = socket.gethostbyname(dest)
        except socket.error as e:
            print("Failed to get address")
            os.popen("dhcpcd -n %s" % interface)
        tries += 1
        sleep(10)

    print(dest_addr + " <-- Finally found it!")

        
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

def test_ap_linux(interface, ap1, ap2, dest):
    ''' Returns "Safe", "Unsafe", or "Possibly unsafe". Could also return IMPOSSIBURU, but should not happen '''
    # Should perform the tests needed.
    # 1. Connect to ap and check it's ip, essid, bssid.
    # 2. Compare to other aps results.
    # 3. If they are the same:
    #       Traceroute to some dest from both APs
    #       if traceroute is the same:
    #           Impossiburu!
    #       else:
    #           Possibly unsafe
    #    else:
    #       if netID is the same:
    #           Safe
    #       else:
    #           Traceroute some dest from both APs
    #           if traceroute is the same:
    #               Possibly unsafe
    #           else: (if there is an extra hop)
    #               Unsafe
    
    # Connect and traceroute APs
    #print(ap1)
    #print(type(ap1))
    #ap1essid = ap1['essid']
    #print(ap1essid)
    #print(type(ap1essid))
    #print(dest)


    # Connect and traceroute AP1
    conap1 = False
    while not conap1: # Since we want to be sure we are connected before we proceed, use a while loop to make sure we connect.
        ap1results = ifiw.ifiw.connect_essid(interface, ap1['essid'], "dhcpcd", True) # Using dhcpcd right now, cause that's what I use for dhcp
        conap1 = ap1results[0]
        print("Ap1 " + ap1['essid'] + " connected: "+ str(conap1))
        sleep(4)
    print(ap1results)


    ap1trace = None
    if conap1:
        print("traceroute AP1" + str(ap1['essid']))
        ap1trace = traceroute(dest, interface)
        print(str(ap1trace)+ "<-- conap1")

    print("Wait for 10 seconds before we connect to the next AP")
    #sleep(10)
    print("Sleep is over! Get to work!")

    # Connect and traceroute AP2
    conap2 = False
    while not conap2:
        ap2results = ifiw.ifiw.connect_essid(interface, ap2['essid'], "dhcpcd", True)
        conap2 = ap2results[0]
        print("Ap2 " + ap2['essid'] + " connected: "+ str(conap2))
        sleep(4)

    ap2trace = None
    if conap2:
        print("traceroute AP2" + str(ap2['essid']) )
        ap2trace = traceroute(dest, interface)
        print(str(ap1trace)+ "<-- conap2")



    # Can't really do the tests  properly..
    if ap1['essid'] == ap2['essid'] and ap1['bssid'] == ap2['bssid']:
#    if True:
        print('The bssid and essid are the same, continue testing')
        if ap1trace[1] == ap2trace[1]:
            print("Access points IPs are the same, check all results of traceroute")
            if ap1trace == ap2trace:
                return "IMPOSSIBURU!"
            else:
                return "Possibly unsafe"
        else:
            print("Access points don't share the same IP, check netID")
            # This actually only checks the netmask for now. But w/e.
            if ap1results[1] == ap2results[1]:
                print("Access points share the same netID (actually checking the netmask right now)")
                return "Safe"
            else:
                if ap1trace == ap2trace:
                    print("Both traceroutes are exactly the same....")
                    return "_Exactly_ the same traceroute..."
                elif len(ap1trace) == len(ap2trace):
                    print("The traceroutes are of the same length.")
                    return "Possibly unsafe"
                elif len(ap1trace) > len(ap2trace):
                    print("ap1trace longer than ap2trace")
                    ret = ap1['essid'] + " has longer trace route, probably rogue. UNSAFE"
                    return ret
                elif len(ap1trace) < len(ap2trace):
                    print("ap2trace longer than ap1trace")
                    ret = ap2['essid'] + " has longer trace route, probably rogue. UNSAFE"
                    return ret
                else:
                    print("Should never get this..")
                    return "Yeah, everything went bad..."







    if ap1['essid'] == ap2['essid']:
        print("Same essid")
    else:
        print("essid not the same")

    if ap1['bssid'] == ap2['bssid']:
        print("Same bssid")
    else:
        print("bssid not  the same")

    if ap1trace[1] == ap2trace[1]:
        print("Same IPs")
    else:
        print("IPs not  the same")

