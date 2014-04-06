import os
import re
import socket
from time import sleep
from subprocess import Popen, PIPE, STDOUT

from wifi_scan_linux.ifiw import misc

# Regular expressions.
_re_mode = (re.I | re.M | re.S)
interface_pattern = re.compile('(.*?) (.*)', _re_mode)
essid_pattern = re.compile('.*ESSID:"?(.*?)".*\n', _re_mode)
channel_pattern = re.compile('.*Channel:?=? ?(\d+)', _re_mode)
freq_pattern = re.compile('.Frequency:(\d.*)\s\(Channel', _re_mode)
bitrates_pattern = re.compile('([\d\.]+)\s+\S+/s', _re_mode)
bssid_pattern = re.compile('.*Address: (.*?)\n', _re_mode)
mode_pattern = re.compile('.*Mode:([A-Za-z-]*?)\n', _re_mode)
wep_pattern = re.compile('.*Encryption key:(.*?)\n', _re_mode)
wpa1_pattern = re.compile('(WPA Version 1)', _re_mode)
altwpa_pattern = re.compile('(wpa_ie)', _re_mode)
wpa2_pattern = re.compile('(WPA2)', _re_mode)
signaldbm_pattern = re.compile('.*Signal level:?=? ?(-\d\d*)', _re_mode)
quality_pattern = re.compile('.*Quality:?=? ?(\d+/?\d+)\s+', _re_mode)

inet_pattern = re.compile('inet (\d*.\d*.\d*.\d*).', _re_mode)
netmask_pattern = re.compile('netmask (\d*.\d*.\d*.\d*).', _re_mode)

altstrength_pattern = re.compile('.*Signal level:?=? ?(\d+)\s*/?\s*(\d*)', _re_mode)
strength_pattern = re.compile('.*Quality:?=? ?(\d+)\s*/?\s*(\d*)', _re_mode)
freqchannel_pattern = re.compile('.*Frequency:(.*?)\n', _re_mode)

class ifiw():
    
    def getInterfaces():
        ''' Returns a list with interface names.

            The search get the info from socket, then strips away the index from the name.
        '''
        interfaces = []
        iface = socket.if_nameindex() # Get the available interfaces from the socket module
        for i in iface: # And only append the name of the interface
            interfaces.append(i[1])

        return interfaces

    def scan(interface):
        ''' Returns a dict.values() of access points. 
            
            Values:
            essid -- Network name
            channel -- Channel number
            frequency -- Frequency (channel frequency)
            quality -- Quality (x/70)
            signal -- Signal level in dBm
            bitrates (list) -- Bitrates the AP can transfer in, sorted lowes->highest
            bssid -- MAC address of the AP
            mode -- What mode the AP operates in
            encrypted -- Returns bool. 
            encryption -- Type of encryption, if any. Available values are: None, WEP, WPA, WPA2
            hidden -- Bool, hidden network == True.

            Takes an interface name as argumnt and performes an 
                % iwlist <interface> scan
            to see available access points.
        '''

        cmd = "iwlist %s scan" % interface
        result = os.popen(cmd)

        # since os.popen returns nothing useful as is, 
        # we take all the info in the return value and put it in a string.
        # We can then split the string appart, separating the networks.
        lines = ""
        for line in result: 
            line = str(line)
            lines = lines + line
        networks = lines.split("   Cell ")

        def __parseAccessPoint(cell): # Helper to get all the info out of the cell.
            ''' Parse the cell for its attributes

                Returns a dict with the attributes.
            '''

            ap = {}
            ap['essid'] = misc.Regex(essid_pattern, cell)
            try:
                ap['essid'] = misc.to_unicode(ap['essid'])
            except (UnicodeDecodeError, UnicodeEncodeError):
                print("UTF-8 conversion troubles! Ignoring!")
                return None
            # Some APs send out their hidden network with a NULL bytes. Strip them off.
            ap['essid'] = ap['essid'].replace('\x00', '')
            if ap['essid'] in ["Hidden", "<hidden>", "", None]:
                ap['hidden'] = True
                ap['essid'] = "<hidden>"
            else:
                ap['hidden'] = False

            # Get the channel
            ap['channel'] = misc.Regex(channel_pattern, cell)

            # Get the frequency
            ap['freq'] = misc.Regex(freq_pattern, cell)

            # Bitrates
            bitrates = cell.split("Bit Rates")[1].replace("\n", ";")
            bitrates2 = cell.split("Bit Rates")[-1].replace("\n", ";")
            m = re.findall(bitrates_pattern, bitrates)
            m = m + re.findall(bitrates_pattern, bitrates2)
            if m:
                # Sort the bitrates
                m.sort(key=lambda m: float(m))
                ap['bitrates'] = m
            else:
                ap['bitrates'] = None

            # BSSID
            ap['bssid'] = misc.Regex(bssid_pattern, cell)

            # Mode
            ap['mode'] = misc.Regex(mode_pattern, cell)

            # Encryptions!
            if misc.Regex(wep_pattern, cell) == 'on':
                # Default to wEP
                ap['encrypted'] = True
                ap['encryption'] = "WEP"
                if misc.Regex(wpa1_pattern, cell) == 'WPA Version 1':
                    ap['encryption'] = 'WPA'

                if misc.Regex(altwpa_pattern, cell) == 'wpa_ie':
                    ap['encryption'] = 'WPA'

                if misc.Regex(wpa2_pattern, cell) == 'WPA2':
                    ap['encryption'] = 'WPA2'
            else:
                ap['encrypted'] = False
                ap['encryption'] = None

            # Signal level
            ap['signal'] = misc.Regex(signaldbm_pattern, cell)

            # Quality
            ap['quality'] = misc.Regex(quality_pattern, cell)


            return ap

        access_points = []
        access_points = {}
        for cell in networks:
            if 'ESSID:' in cell: # Only get the cells containing an ESSID.
                entry = __parseAccessPoint(cell) # Get all the cells attributes
                if entry != None: # If has attributes, we want to add it to the list.
                   # access_points.append(entry)
                   access_points[entry['bssid']] = entry

                #    access_points[entry['bssid']] = entry

        return access_points.values()


    # dhcpcd is giving some seriouse problems with the connecting, makitg the whole program fail.
    # Not sure have to solve it all... Sometimes it works, sometimes not. It's like russian roulette.
    def connect_essid(interface, essid, dhcp, restart=False, kill=False):
        ''' Connects to a network
            interface -- The interface to use
            essid -- The network
            dhcp -- The dhcp client to use.

            dhcp options:
                dhclient
                dhcpd
        '''

        # Select the propers dhcp-command.
        if dhcp == 'dhclient':
            dhcp_cmd = 'dhclient %s' % interface
        elif dhcp == 'dhcpcd':
            if restart:
                dhcp_cmd = 'dhcpcd -nK -t 0 --noipv4ll %s' % interface
            else:
                dhcp_cmd = 'dhcpcd -K -t 0 --noipv4ll %s ' % interface
            if kill:
                dhcp_kill = 'dhcpcd -k -x %s' % interface
            else:
                dhcp_kill = ""
        else:
            dhcp_cmd = ""



        # Bring the interface down first, so we disconnect any existing connection.
        os.popen(dhcp_kill)
        down = 'ifconfig %s down' % interface
        up = 'ifconfig %s up' % interface
        os.popen(down)
        os.popen(up)



        net = 'iwconfig ' + interface + ' essid "' + essid +'"'
        #print(net)
        os.popen(net)
        os.popen(dhcp_cmd)

        inet = ""
        netmask = ""
        inet_cmd = 'ifconfig ' + interface
        while inet == "" or inet == None:
            result = os.popen(inet_cmd)
            lines = ""
            for line in result: 
                line = str(line)
                lines = lines + line

            #print(lines)
            inet = misc.Regex(inet_pattern, lines)
            netmask = misc.Regex(netmask_pattern, lines)
            #print(net)
            #print(str(inet) + " <-- inet, connecting to " + essid)
            sleep(1)

        results = []
        if inet != "" or inet != None:
            results.append(True)
            results.append(netmask)
            return results
        else:
            results.append(False)
            results.append(netmask)
            return results
    def disconnect(interface, dhcp):
        if dhcp == 'dhclient':
            dhcp_cmd = ' %s' % interface
        elif dhcp == 'dhcpcd':
            dhcp_cmd = 'dhcpcd -x %s' % interface
        else:
            dhcp_cmd = ""





    





#test = ifiw.getInterfaces()
#print(test)
#aps = ifiw.scan(test[2])
#keys = list(aps)
#aa = list(aps)
#con = ""
#for a in aa:
#    if a['encrypted'] == False:
#        con = ifiw.connect_essid(test[2], a['essid'], 'dhcpcd')
#print(aa)
#con = ifiw.connect_essid(test[2], m['essid'], 'dhcpcd')


#print(keys)
#for ap in aps:
#    print(str(ap['essid']) + " - " + str(ap['bssid']) + " - Encrypted: "+str(ap['encrypted']) + " " + str(ap['encryption'])+" - " + str(ap['signal']) +"dBm - " + str(ap['quality'])+" - Channel: "+ str(ap['channel'])+"("+ ap['freq']+") - Mode: "+ap['mode'] + " - Hidden: " + str(ap['hidden']) + " - Bitrates: "+ str(ap['bitrates']))
#print(aps)
