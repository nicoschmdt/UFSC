import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.ButtonGroup;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;

public class Interface extends JFrame{
	private String[] levels = {"Easy","Medium","Hard"}; 
	private JMenu file_Menu;
	private JMenuItem about;
	private JMenu difficult;
	private JMenuBar bar;
	private JRadioButtonMenuItem[] level; // think of a better name
	private ButtonGroup levelButtonGroup;
	private Map map;
	// I believe I have to add a JPanel(?)
	private JPanel panel;
	//trying to add the select level
	private String selected_difficult = "Easy";
	
	public Interface() {
		super("Minesweeper");
		//PANEL
		setLayout(new FlowLayout());
		
		panel = new JPanel(new BorderLayout());
		panel.setPreferredSize(new Dimension(600,600));
		//
		
		file_Menu = new JMenu("File");
		file_Menu.setMnemonic('F');
		about = new JMenuItem("About");
		file_Menu.add(about);
		file_Menu.addSeparator();
		
		// choose if its going to be hard, medium or easy mode
		//maybe I can add smth like Challenge thats just impossible cuz itd be fun
		difficult = new JMenu("Difficult");
		file_Menu.add(difficult);
		//choosing the difficult
		level = new JRadioButtonMenuItem[levels.length];
		levelButtonGroup = new ButtonGroup();
		for(int i = 0; i < levels.length; i++) {
			if(i == 0) {
				level[i] = new JRadioButtonMenuItem(levels[i],true);
			}else {
				level[i] = new JRadioButtonMenuItem(levels[i]);
			}
			difficult.add(level[i]);
			levelButtonGroup.add(level[i]);
//			level[i].addActionListener(levelHandler); // still have to do this part
		}
		
		//the about actionListener
		about.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(Interface.this,
						"Hello!\n\nIf you have never played Minesweeper before here is what you have to do!\nTry clicking the buttons bellow, you'll see that it appears a number\nthis number show the quantity of bombs near the place you just clicked\nyour objective is to clear all the area that doesn't have bombs!\n\n Good luck!",
						"About",JOptionPane.PLAIN_MESSAGE);
			}
		});
		bar = new JMenuBar();
		setJMenuBar(bar);
		bar.add(file_Menu);
		
		//map
		map = new Map();
		panel.add(map);
		super.add(panel);
		
		
	}
	public void set_difficulty(String s) {
		selected_difficult = s;
	}
	public String get_difficulty() {
		return selected_difficult;
	}
	
	//main
	public static void main(String[] args) {
		Interface window = new Interface();
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setSize(1000,1000);
		window.setVisible(true);
	}
}
