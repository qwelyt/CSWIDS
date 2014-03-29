#!/usr/bin/python3

from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="CSWIDS - Client-Side Wireless Intrusion Detection System")
        self.set_border_width(6)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.button_box = Gtk.Box(spacing=6)
        self.vbox.pack_start(self.button_box, True, True, 6)

        header = self.header_bar()
        self.set_titlebar(header)

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
        liststore = Gtk.ListStore(str, str, str, str, str)

        # Populate list with dummy values for now.
        for i in range(1,10):
            name = "AP"+ str(i)
            strength = i*10
            encryption = "None"
            mac = "::"+ str(i)
            channel = str(i)
            liststore.append([name, str(strength)+"%", encryption, mac, channel])

        # To list the APs as going from best signal to weakest, we need to sort it.
        # These two lines does that.
        sorted_model = Gtk.TreeModelSort(model=liststore)
        sorted_model.set_sort_column_id(1, Gtk.SortType.DESCENDING)

        treeview = Gtk.TreeView(model=sorted_model)
        #treeview = Gtk.TreeView(model=liststore)
        treeview.set_headers_clickable(True)

        treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        select = treeview.get_selection()
        select.connect("changed", self.on_ap_selection_changed)

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

        self.vbox.pack_start(treeview, True, True, 0)

    def log_area(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.vbox.pack_start(scrolledwindow, True, True,6)

        textview = Gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text("This is the log.")
        #textbuffer.set_editable(False)
        scrolledwindow.add(textview)

    def on_ap_selection_changed(self, selection):
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


win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
