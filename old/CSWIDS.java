import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class CSWIDS extends JFrame{
	private JMenuBar menuBar;
	private JMenu menu;
	private JMenuItem iQuit;

	private JPanel buttonBar, main;
	private JButton bTest;

	private JTextArea log;
	private JList apList;
	//private ArrayList<String> apData;
	private DefaultListModel apData;


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
		for(int i=0; i< 10; i++)
			apData.addElement("ap"+i);
		apList = new JList(apData);
		apList.setSelectionModel(new setSelectionModel(apList,2));
		apList.setLayoutOrientation(JList.VERTICAL);
		apList.setVisibleRowCount(10);
		JScrollPane spAP = new JScrollPane(apList);
		spAP.setPreferredSize(new Dimension(20, 150));



		log = new JTextArea(10,50);
		log.setLineWrap(true);
		log.setEditable(false);
		JScrollPane spLog = new JScrollPane(log);
		log.append("This is where the log information will be outputed.");

		main.add(spAP);
		main.add(spLog);
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

		bTest.addActionListener(lis);

		buttonBar.add(bTest);

		add(buttonBar, BorderLayout.NORTH);
	}

	class Events implements ActionListener{
		public void actionPerformed(ActionEvent ae){
			if(ae.getSource() == iQuit){
				dispose();
				System.exit(0);
			}
		}
	}

	public static void main(String[] args){
		new CSWIDS().init();
	}

	private static class setSelectionModel extends DefaultListSelectionModel{
		private JList list;
		private int maxCount;

		private setSelectionModel(JList list,int maxCount){
			this.list = list;
			this.maxCount = maxCount;
		}

		@Override
		public void setSelectionInterval(int index0, int index1){
			if (index1 - index0 >= maxCount){
			index1 = index0 + maxCount - 1;
			}
			super.setSelectionInterval(index0, index1);
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
