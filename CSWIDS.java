import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class CSWIDS extends JFrame{
	private JMenuBar menuBar;
	private JMenu menu;
	private JMenuItem iQuit;

	private JPanel buttonBar;
	private JButton bTest, bQuit;


	public void init(){
		setTitle("CSWIDS");
		menuBar();
		buttonBar();

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
