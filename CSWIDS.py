#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import sys
import socket

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="CSWIDS - Client-Side Wireless Intrusion Detection System")
        self.set_border_width(6)
        #self.set_default_size(200, 400)
        self.selected_items = []
        self.os = sys.platform # Check what OS we are on
        self.interfaces = socket.if_nameindex() # List available  network interfaces
        self.selected_interface = None
        self.found_access_points = None
        self.entry = Gtk.Entry()
        self.entry.set_text("dsv.su.se")

        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.button_box = Gtk.Box(spacing=6, homogeneous=True)
        self.vbox.pack_start(self.button_box, False, False, 6)

        header = self.header_bar()
        self.set_titlebar(header)

        # SSID, Strength, Encryption, MAC, channel, frequency, (list)bitrate, mode
        # 8 strs for the liststore. The  bitrate attribute for networks is a list, so show it in a combobox.
        self.liststore = Gtk.ListStore(str, int, str, str, str, str, str, str)
        self.liststore_bitrates = Gtk.ListStore(str)
        self.textview = Gtk.TextView()

        self.button_bar()
        self.ap_list()
        self.log_area()

        self.add(self.vbox)

    def header_bar(self):
        #print("header_bar called.")
        
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "CSWIDS"
        hb.props.subtitle = "Client-Side Wireless Intrusion Detection System"

        return hb


    def button_bar(self):
        #button = Gtk.Button(label="Quit")
        #button.connect("clicked", Gtk.main_quit)
        #self.button_box.pack_start(button, True, True, 0)

        interface_list = Gtk.ListStore(int, str)
        for interface in list(self.interfaces):
            interface_list.append(interface)
        combo_box = Gtk.ComboBox.new_with_model(interface_list)
        combo_box.connect("changed", self.selected_interface_changed)
        render_text = Gtk.CellRendererText()
        combo_box.pack_start(render_text, True)
        combo_box.add_attribute(render_text, "text", 1)
        self.button_box.pack_start(combo_box, True, True, 0)


        button = Gtk.Button(label="Scan")
        button.connect("clicked", self.scan_for_networks)
        self.button_box.pack_start(button, True,True, 0)

        sitebox = Gtk.Box()
        label = Gtk.Label("Test site:")
        sitebox.pack_start(label, True, True, 0)
        sitebox.pack_start(self.entry, True, True, 0)
        self.button_box.pack_start(sitebox, True, True, 0)


        button = Gtk.Button(label="Test")
        button.connect("clicked", self.test_selected_aps)
        self.button_box.pack_start(button, True, True, 0)

    def ap_list(self):
        # To list the APs as going from best signal to weakest, we need to sort it.
        # These two lines does that.
        sorted_model = Gtk.TreeModelSort(model=self.liststore)
        sorted_model.set_sort_column_id(1, Gtk.SortType.DESCENDING)

        treeview = Gtk.TreeView(model=sorted_model)
        #treeview = Gtk.TreeView(model=liststore)
        treeview.set_headers_clickable(True)

        treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        #treeview.get_selection().set_select_function()
        select = treeview.get_selection()
        global ap_selection_signal
        ap_selection_signal = select.connect("changed", self.on_ap_selection_changed)

        # SSID, Strength, Encryption, MAC, channel, frequency, (list)bitrate, mode
        renderText = Gtk.CellRendererText()

        column_name = Gtk.TreeViewColumn("ESSID", renderText, text=0)
        treeview.append_column(column_name)

        column_strength = Gtk.TreeViewColumn("Strength", renderText, text=1)
        treeview.append_column(column_strength)

        column_enc = Gtk.TreeViewColumn("Encryption", renderText, text=2)
        treeview.append_column(column_enc)

        column_mac = Gtk.TreeViewColumn("BSSID", renderText, text=3)
        treeview.append_column(column_mac)

        column_chan = Gtk.TreeViewColumn("Channel", renderText, text=4)
        treeview.append_column(column_chan)

        column_freq = Gtk.TreeViewColumn("Frequency", renderText, text=5)
        treeview.append_column(column_freq)

        renderCombo = Gtk.CellRendererCombo()
        renderCombo.set_property("editable", True)
        renderCombo.set_property("model", self.liststore_bitrates)
        renderCombo.set_property("text-column", 0)
        renderCombo.set_property("has-entry", False)
        column_bit = Gtk.TreeViewColumn("Bitrates", renderCombo, text=6)
        treeview.append_column(column_bit)

        column_mode = Gtk.TreeViewColumn("Mode", renderText, text=7)
        treeview.append_column(column_mode)
        treeview.set_size_request(400,200)

        #list_size = Gtk.Adjustment(lower=10, page_size=100)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(treeview)
        scrolledwindow.set_min_content_width(1000)
        scrolledwindow.set_min_content_height(400)

        self.vbox.pack_start(scrolledwindow, True, True, 0)
        #self.vbox.pack_start(treeview, True, True, 0)

    def log_area(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.vbox.pack_start(scrolledwindow, True, True,6)

        textbuffer = self.textview.get_buffer()
        self.textview.set_editable(False) # Disable user editing the log
        self.textview.set_cursor_visible(False) # Remove cursor from log
        scrolledwindow.add(self.textview)

    def selected_interface_changed(self, selection):
        tree_iter = selection.get_active_iter()
        if tree_iter != None:
            model = selection.get_model()
            self.selected_interface = model[tree_iter][1]
        
        print(self.selected_interface)
        


    def on_ap_selection_changed(self, selection):
        liststores, listpaths = selection.get_selected_rows()
        self.selected_items.clear()
        for x in listpaths:
            a = liststores.get_iter(x)
            value = liststores.get_value(a, 0)
            self.selected_items.append(value)

        if len(listpaths) > 2:
            for row in range(len(listpaths)):
                if listpaths[row][0] is not row:
                    selection.handler_block(ap_selection_signal)
                    selection.unselect_path(listpaths[row])
                    selection.handler_unblock(ap_selection_signal)

        #for selected_row in range(len(listpaths)):
        #    if listpaths[selected_row][0] == 1:
        #        selection.handler_block(ap_selection_signal)
        #        selection.unselect_path(listpaths[selected_row])
        #        selection.handler_unblock(ap_selection_signal)
        '''
        model, treeiter = selection.get_selected_rows()
        number = 0
        for x in treeiter:
            number+=1
            a = model.get_iter(x)
            value = model.get_value(a, 0)
            print("Selected", value)

        print(number,"in total")

        #if treeiter != None:
         #   print("You selected", model[treeiter][0])
         '''

    def scan_for_networks(self, widget):
        textbuffer = self.textview.get_buffer()
        if self.selected_interface != None:
            textbuffer.insert(textbuffer.get_end_iter(), "Scan initiated...")

            # Clear the old values
            self.liststore.clear()
            

            # SSID, Strength, Encryption, MAC, channel, frequency, (list)bitrate, mode
            if self.os == "linux":
                #print("LIIIIINUUUUX!!!")
                #from . 
                from wifi_scan_linux import wifi_scan_linux
                # Here is where the actuall scan should occur
                self.found_access_points = wifi_scan_linux.scan(self.selected_interface)
                found_aps = self.found_access_points
                #print(found_aps)
                for a in found_aps:
                    essid = a['essid']
                    bssid = a['bssid']
                    encryption = str(a['encryption'])
                    mode = a['mode']
                    freq = a['freq']
                    quality = a['quality']
                    signal = a['signal']
                    chan = str(a['channel'])
                    bitrates = a['bitrates']
                    rates = ""
                    i = 0
                    for rate in bitrates:
                        i += 1
                        rates = rates + rate + ", "
                        if i % 4 == 0:
                            rates = rates +"\n"

                    if rates[-1] == "\n":
                        rates = rates[:-2]

                    #strength=float(signal)
                    qual = quality.split("/")
                    strength = float(float(qual[0])/float(qual[1]))*100

                    self.liststore.append([essid, strength, encryption, bssid, chan, freq, rates, mode])
                '''  ssid = a.ssid.encode('utf-8').decode('utf-8')
                    signal = a.signal
                    freq = a.frequency
                    bitrate = a.bitrates
                    if a.encrypted:
                        enc = a.encryption_type
                    else:
                        enc = 'Unsecure'

                    chan = a.channel
                    addr = a.address
                    mode = a.mode
                    # Signal strength conversion: From dBm (range -100 to -50) to percentage (range 0 to 100)
                    # quality = 2*(dBm + 100)
                    if signal <= -100:
                        strength = 100
                    elif signal >= -50:
                        strength = 0
                    else:
                        strength=2*(signal+100)
                    strength=2*(signal+100)
                    for rate in bitrate:
                        self.liststore_bitrates.append([rate])
                        #print(rate)
                    #print("SSID "+ssid + " Strength: "+str(strength)+"% Frequency:"+ str(freq) + " Bitrate:"+ str(bitrate)+" Encryption: "+ str(enc)+" Channel: "+str(chan)+" MAC: "+addr+" Mode: "+mode)
                    self.liststore.append([ssid, strength, enc, addr, str(chan), freq, "See bitrate", mode])
                    '''




            # Populate list with dummy values for now.
            #for i in range(1,10):
            #    name = "AP"+ str(i)
            #    strength = i*10
            #    encryption = "None"
            #    mac = "bc:5f:c3:96:71:a"+ str(i)
            #    channel = str(i)
            #    self.liststore.append([name, str(strength)+"%", encryption, mac, channel])

            textbuffer.insert(textbuffer.get_end_iter(), " Done!\n")

        else:
            textbuffer.insert(textbuffer.get_end_iter(), "No interface selected.\n")

    def test_selected_aps(self, widget):
        #print(self.selected_items)
        textbuffer = self.textview.get_buffer()
        dest = self.entry.get_text()
        if len(self.selected_items) != 2:
            textbuffer.insert(textbuffer.get_end_iter(), "You need to select 2 access points to be able to test.\n")
        if dest == "":
            textbuffer.insert(textbuffer.get_end_iter(), "You need to specify a url or IP to test aginst.\n")
        if len(self.selected_items) == 2 and dest != "":
            print_items = self.selected_items
            ap1 = print_items.pop(0)
            ap2 = print_items.pop(0)
            self.selected_items.append(ap1) # Put them back in the selected_items list so you can press "Test" again.
            self.selected_items.append(ap2)
            for ap in self.found_access_points:
                if ap['essid'] == ap1:
                    ap1 = ap
                if ap['essid'] == ap2:
                    ap2 = ap
            textbuffer.insert(textbuffer.get_end_iter(), "Test on: "+ ap1['essid'] + " and " + ap2['essid'] + ". Against: "+ dest+".\n")
            if self.os == "linux":
                from wifi_scan_linux import wifi_scan_linux
                result = wifi_scan_linux.test_ap_linux(self.selected_interface, ap1, ap2, dest)

            textbuffer.insert(textbuffer.get_end_iter(), result +"\n")

        

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
