from wifi_scan_linux.ifiw import ifiw

def scan(interface):
    ''' Returns all found access points '''
    aps = ifiw.ifiw.scan(interface)
    return aps

def test_ap_linux(ap):
    return None
