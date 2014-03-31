from wifi import Cell

def scan_linux(interface):
    access_points = Cell.all(interface)

    return access_points

def test_ap_linux(ap):
    return None
