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

        self.liststore = Gtk.ListStore(str, str, str, str, str)
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
        button = Gtk.Button(label="Quit")
        button.connect("clicked", Gtk.main_quit)
        self.button_box.pack_start(button, True, True, 0)

        button = Gtk.Button(label="Test")
        #button.connect("clicked", doTheTestsFunktion)
        self.button_box.pack_start(button, True, True, 0)

        button = Gtk.Button(label="Scan")
        button.connect("clicked", self.scan_for_networks)
        self.button_box.pack_start(button, True,True, 0)

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

        textbuffer = self.textview.get_buffer()
        #textbuffer.set_text("This is the log.\n")
        #textbuffer.set_editable(False)
        scrolledwindow.add(self.textview)


    def on_ap_selection_changed(self, selection):
        liststores, listpaths = selection.get_selected_rows()
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
        textbuffer.insert(textbuffer.get_end_iter(), "Scan initiated\n")
        # Clear the old values
        self.liststore.clear()

        # Populate list with dummy values for now.
        for i in range(1,10):
            name = "AP"+ str(i)
            strength = i*10
            encryption = "None"
            mac = "::"+ str(i)
            channel = str(i)
            self.liststore.append([name, str(strength)+"%", encryption, mac, channel])

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
