#!/usr/bin/python3

from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="CSWIDS - Client-Side Wireless Intrusion Detection System")
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.button_box = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.button_box, True, True, 6)

        self.header_bar()
        self.button_bar()
        self.ap_list()
        self.log_area()

    def header_bar(self):
        print("header_bar called.")

    def button_bar(self):
        button = Gtk.Button(label="Quit")
        button.connect("clicked", Gtk.main_quit)
        self.button_box.pack_start(button, True, True, 0)

        button = Gtk.Button(label="Test")
        #button.connect("clicked", doTheTestsFunktion)
        self.button_box.pack_start(button, True, True, 0)

        button = Gtk.Button(label="Scan")
        #button.connect("clicked", scanFärNetworksFunction)
        self.button_box.pack_start(button, True,True, 0)

    def ap_list(self):
        liststore = Gtk.ListStore(str, str)
        # Dummy list
        for i in range(1,10):
            name = "AP"+ str(i)
            mac = "::"+ str(i)
            liststore.append([name, mac])
            #self.liststore.append(["Name", "MAC"])

        treeview = Gtk.TreeView(model=liststore)

        renderText = Gtk.CellRendererText()
        columnESSID = Gtk.TreeViewColumn("ESSID", renderText, text=0)
        treeview.append_column(columnESSID)

        columnBSSID = Gtk.TreeViewColumn("BSSID", renderText, text=1)
        treeview.append_column(columnBSSID)

        self.vbox.pack_start(treeview, True, True, 0)

    def log_area(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.vbox.pack_start(scrolledwindow, True, True,6)

        textview = Gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text("This is the log.")
        textbuffer.set_editable(False)
        scrolledwindow.add(textview)

win = MainWindow()
win.connect("delete-entry", Gtk.main_quit)
win.show_all()
Gtk.main()
