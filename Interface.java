import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import javax.swing.AbstractButton;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.SwingConstants;
import javax.swing.Timer;
import javax.swing.plaf.basic.BasicComboBoxUI.ItemHandler;

public class Interface {
	private String[] levels = {"Easy","Medium","Hard"}; 
	private JMenu file_Menu;
	private JMenuItem about;
	private JMenu difficult;
	private JMenuBar bar;
	private JFrame frame;
	private JRadioButtonMenuItem[] level; // think of a better name
	private ButtonGroup levelButtonGroup;
	private Map map;
	private JPanel panel,panel_two;
	//trying to add the select level
	private String selected_difficult = "Easy";
	//
	private JLabel label_bombs,label_timer;
	private JButton restart_b;
	private Box box;
	private int counter = 0;
	private int stats = 0;
	//listener menu

	private boolean game_lost = false; //if the game is lost this'll turn true gotta use this to stop the timer
	
	public Interface() {
		//PANEL

		frame = new JFrame("Minesweeper");
		frame.setLayout(new BorderLayout());
				
		panel = new JPanel(new FlowLayout());
		panel.setPreferredSize(new Dimension(250,200));
		panel.setBackground(Color.DARK_GRAY);
		//test 1506 I'm trying to add the bombs panel but idk how to do this
		//I managed to add another panel but still it remained as a wip
		panel_two = new JPanel();
		
		panel_two.setPreferredSize(new Dimension(50,50));
		panel_two.setBackground(Color.YELLOW);
		panel_two.setLayout(new BoxLayout(panel_two,BoxLayout.X_AXIS));
		panel_two.setBorder(BorderFactory.createEmptyBorder(0,10,10,10));
		//it'll have to say how many undentified bombs are in the map
		//gotta make a method for that
		//box
		box = Box.createHorizontalBox();
		//
		label_bombs = new JLabel();
		label_bombs.setText("Bombs remaining: ");
		label_timer = new JLabel();
		new Timer(1000, new ActionListener() {

		      @Override
		      public void actionPerformed(ActionEvent e) {
		    	  
		    	  label_timer.setText("Time Passed: " + counter);
				  counter++;
		      }
		    }).start();
		
		box.add(label_bombs);
		box.add(Box.createHorizontalStrut(110));
		//gotta fix the size, cant really set this in i3 :/
		restart_b = new JButton("Restart");
		restart_b.setPreferredSize(new Dimension(40,40));
		restart_b.addActionListener((e) -> {
			this.counter = 0;
			map = new Map(stats);
			this.game_lost = false;
			panel.removeAll();
			panel.add(map,BorderLayout.CENTER);
			panel.repaint();			
		});
		box.add(restart_b);
		box.add(Box.createHorizontalStrut(110));
		//
		box.add(label_timer);
		panel_two.add(box);
		//
		
		file_Menu = new JMenu("File");
		file_Menu.setMnemonic('F');
		about = new JMenuItem("About");
		file_Menu.add(about);
		file_Menu.addSeparator();
		
		// choose if its going to be hard, medium or easy mode
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
			level[i].addItemListener((e) -> {
				AbstractButton btn = (AbstractButton)e.getSource();
				String text = btn.getText();
				if(text.equals("Easy")) {
					map = new Map(0);
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 0;
				}else if(text.equals("Medium")) {
					map = new Map(1);
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 1;
				}else {
					map = new Map(2);
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 2;
				}

			});
		}
		level[0].setSelected(true);
		
		//the about actionListener
		about.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null,
						"Hello!\n\nIf you have never played Minesweeper before here is what you have to do!\nTry clicking the buttons bellow, you'll see that it appears a number\nthis number show the quantity of bombs near the place you just clicked\nyour objective is to clear all the area that doesn't have bombs!\n\n Good luck!",
						"About",JOptionPane.PLAIN_MESSAGE);
				
			}
		});
		bar = new JMenuBar();
		bar.add(file_Menu);
		
		//map
		map = new Map(0);
		panel.add(map,BorderLayout.CENTER);
		//frame add
		frame.setJMenuBar(bar);
		frame.add(panel_two,BorderLayout.PAGE_START);
		frame.add(panel,BorderLayout.CENTER);
		
		//basic
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(600,400);
		frame.setVisible(true);

		
		
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
	}
}