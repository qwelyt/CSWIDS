import javax.swing.*;
import javax.swing.event.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.Date.*;
import java.text.SimpleDateFormat;

public class CSWIDS extends JFrame{
	private JMenuBar menuBar;
	private JMenu menu;
	private JMenuItem iQuit;

	private JPanel buttonBar, main;
	private JButton bTest, bScan;

	private JTextArea log;
	private JList apList;
	//private ArrayList<String> apData;
	private DefaultListModel apData;
	private ListSelectionModel ListSM;


	private Date time;


	public void init(){
		setTitle("CSWIDS");
		menuBar();
		buttonBar();

		main = new JPanel();
		main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));

		/*
		tmpTxt = new JTextArea(10,50);
		tmpTxt.setLineWrap(true);
		tmpTxt.setEditable(false);
		JScrollPane sp = new JScrollPane(tmpTxt);
		tmpTxt.append("Here is where the AP should be shown");
		*/

		//apData = new ArrayList<String>("ap1","ap2","ap3");
		apData = new DefaultListModel();

		apList = new JList(apData);
		apList.setSelectionModel(new NumberSelectionModel(apList,2));

		ListSM = apList.getSelectionModel();
		ListSM.addListSelectionListener(new ListSelection());

		apList.setLayoutOrientation(JList.VERTICAL);
		apList.setVisibleRowCount(10);
		JScrollPane spAP = new JScrollPane(apList);
		spAP.setPreferredSize(new Dimension(20, 150));



		log = new JTextArea(10,50);
		log.setLineWrap(true);
		log.setEditable(false);
		JScrollPane spLog = new JScrollPane(log);
		//log.append("This is where the log information will be outputed.");
		
		JSplitPane sPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, spAP, spLog);
		sPane.setResizeWeight(0.5);

		//main.add(spAP);
		//main.add(spLog);
		main.add(sPane);
		add(main);

		setDefaultCloseOperation(EXIT_ON_CLOSE);
		pack();
		setLocationRelativeTo(null);
		setVisible(true);
	}

	private void menuBar(){
		Events lis = new Events(); // Action listener

		menuBar = new JMenuBar();

		menu = new JMenu("Menu");
		menu.getAccessibleContext().setAccessibleDescription("It's a menu!");
		menuBar.add(menu);

		iQuit = new JMenuItem("Quit");
		iQuit.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_Q, ActionEvent.CTRL_MASK)); // CTRL+Q quits
		iQuit.addActionListener(lis);
		menu.add(iQuit);

		setJMenuBar(menuBar);

	}

	private void buttonBar(){
		Events lis = new Events();

		buttonBar = new JPanel();
		bTest = new JButton("Test APs");
		bTest.setEnabled(false);
		bScan = new JButton("Scan for APs");

		bTest.addActionListener(lis);
		bScan.addActionListener(lis);

		buttonBar.add(bTest);
		buttonBar.add(bScan);

		add(buttonBar, BorderLayout.NORTH);
	}

	class Events implements ActionListener{
		public void actionPerformed(ActionEvent ae){
			time = new Date();
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
			String showTime = sdf.format(time);
			log.append(showTime+"\t"); // Print timestamps
			if(ae.getSource() == iQuit){
				dispose();
				System.exit(0);
			}

			else if(ae.getSource() == bTest){
				//int[] selectedAPs = apList.getSelectedIndices();
				//log.append("APs: " + selectedAPs[0] + " and " + selectedAPs[1] + " being tested.\n");
				java.util.List<Object> selectedAPs = apList.getSelectedValuesList();
				log.append("APs: " + selectedAPs.get(0) + " and " + selectedAPs.get(1) + " being tested.\n");
			}
			else if(ae.getSource() == bScan){
				log.append("Scan for networks\n");
				// Ploy method to get APs in the list.
				
				// The actual scan should probably be done here, or after the removing of old APs.

				apData.removeAllElements(); // Clear the old list before populating it with new APs.
				for(int i=0; i< 10; i++)
					apData.addElement("ap"+i);
			}
		}
	}

	class ListSelection implements ListSelectionListener{
		public void valueChanged(ListSelectionEvent e){
			ListSelectionModel lsm = (ListSelectionModel)e.getSource();

			int firstIndex = e.getFirstIndex();
			int lastIndex = e.getLastIndex();
			boolean isAdjusting = e.getValueIsAdjusting();

			if(lsm.isSelectionEmpty()){
				bTest.setEnabled(false); // No APs selected == No testing should be able to be done.
			}
			else{
				int minIndex = lsm.getMinSelectionIndex();
				int maxIndex = lsm.getMaxSelectionIndex();
				for(int i = minIndex; i<=maxIndex; i++){
					if(i > minIndex)
						bTest.setEnabled(true);
					else
						bTest.setEnabled(false);
				}
			}
		}
	}

	public static void main(String[] args){
		new CSWIDS().init();
	}

	private static class NumberSelectionModel extends DefaultListSelectionModel{
		private JList list;
		private int maxCount;

		private NumberSelectionModel(JList list,int maxCount){
			this.list = list;
			this.maxCount = maxCount;
		}

		/*
		@Override
		public void setSelectionInterval(int index0, int index1){
			if (index1 - index0 >= maxCount){
				index1 = index0 + maxCount - 1;
			}
			super.setSelectionInterval(index0, index1);
		}
		*/
		@Override
		public void setSelectionInterval(int index0, int index1){
			if(list.isSelectedIndex(index0)){
				list.removeSelectionInterval(index0,index1);
			}
			else{
				list.addSelectionInterval(index0,index1);
			}
		}

		@Override
		public void addSelectionInterval(int index0, int index1){
			int selectionLength = list.getSelectedIndices().length;
			if (selectionLength >= maxCount)
				return;
		
			if (index1 - index0 >= maxCount - selectionLength){
				index1 = index0 + maxCount - 1 - selectionLength;
			}
			if (index1 < index0)
				return;
			super.addSelectionInterval(index0, index1);
		}
	}
}
