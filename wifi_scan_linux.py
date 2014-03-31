from wifi import Cell

def wifi_scan_linux(interface):
    access_points = Cell.all(interface)

    return access_points

def test_ap_linux(ap):
    return None
