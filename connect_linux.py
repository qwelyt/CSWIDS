from wifi import Cell, Scheme

def connect(interface, found_aps, selected_ap):
    #access_points = Cell.all(interface)
    found_aps = Cell.all(interface)
    print("In connect_linux.connect\n")
    #print(list(found_aps))
    for ap in found_aps:
        print("Checking " + ap.ssid)
        if ap.ssid == selected_ap:
            print("MATCH")
            print("Trying to connect to "+ap.ssid)
            scheme = Scheme.for_cell(interface, 'net', ap)
            results = scheme.activate()
            print(results)

        print("Check done.\n")

    print("For-loop ended.\n")



