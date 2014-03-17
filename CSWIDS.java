import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class CSWIDS extends JFrame{
	private JMenuBar menuBar;
	private JMenu menu;
	private JMenuItem iQuit;

	private JPanel buttonBar, main;
	private JButton bTest;

	private JTextArea tmpTxt, log;

	public void init(){
		setTitle("CSWIDS");
		menuBar();
		buttonBar();

		main = new JPanel();
		main.setLayout(new BoxLayout(main, BoxLayout.Y_AXIS));

		tmpTxt = new JTextArea(10,50);
		tmpTxt.setLineWrap(true);
		tmpTxt.setEditable(false);
		JScrollPane sp = new JScrollPane(tmpTxt);
		tmpTxt.append("Here is where the AP should be shown");

		log = new JTextArea(10,50);
		log.setLineWrap(true);
		log.setEditable(false);
		JScrollPane spLog = new JScrollPane(log);
		log.append("This is where the log information will be outputed.");

		main.add(sp);
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
}
