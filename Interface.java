import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

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
import javax.swing.JTextArea;
import javax.swing.Timer;

public class Interface {
	private String[] levels = {"Easy","Medium","Hard"}; 
	private JMenu file_Menu;
	private JMenuItem about,score;
	private JMenu difficult;
	private JMenuBar bar;
	private JFrame frame,frame_score;
	private JRadioButtonMenuItem[] level; // think of a better name
	private ButtonGroup levelButtonGroup;
	private Map map;
	private JPanel panel,panel_two,panel_score;
	private String selected_difficult = "Easy";
	private JLabel label_bombs,label_timer;
	private JButton restart_b;
	private Box box;
	private int counter = 0;
	private int stats = 0;
	private String info;
	private Score data;
	private JTextArea text_area;
	private File file;
	private int a = 0;
	 //if the game is lost this'll turn true gotta use this to stop the timer
	
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
		label_timer = new JLabel();
		//
		map = new Map(0);
		data = new Score();
		data.set_difficulty("Easy");
		
		//
		new Timer(1000, new ActionListener() {

		      @Override
		      public void actionPerformed(ActionEvent e) {
		    	  
		    	  label_timer.setText("Time Passed: " + counter);
				  if(!map.get_game_lost() && !map.get_game_won()) {
					  counter++;  
				  }
				  data.set_time(counter);
				   //essa variavel é so para nao permitir q isso entre mais de uma vez
				  if(a == 0 && map.get_game_won()) {
					  String n = JOptionPane.showInputDialog("What is your name?"); //n = name
					  data.set_name(n);
					  a = 1;
				  }
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
			map.set_game_lost(false);
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
		score = new JMenuItem("Score");
		file_Menu.add(score);
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
					data.set_difficulty("Easy");
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 0;
					label_bombs.setText("Bombs remaining: " + map.get_qtd_bombs());
				}else if(text.equals("Medium")) {
					map = new Map(1);
					data.set_difficulty("Medium");
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 1;
					label_bombs.setText("Bombs remaining: " + map.get_qtd_bombs());
				}else {
					map = new Map(2);
					data.set_difficulty("Hard");
					panel.removeAll();
					panel.add(map,BorderLayout.CENTER);
					panel.repaint();
					this.stats = 2;
					label_bombs.setText("Bombs remaining: " + map.get_qtd_bombs());
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
		
		score.addActionListener((e) -> {
			
			frame_score = new JFrame("Score");
			panel_score = new JPanel();
			text_area = new JTextArea();
			text_area.setEditable(false);
			
			//
			ReadFile read = new ReadFile();//is it needed?
			WriteFile write = new WriteFile();
			//idk if this goes here tho, since its a writer and I want a reader
			PrintWriter writer;
			file = new File("score.txt");
			
			try {
				writer = new PrintWriter(file,"UTF-8");
				write.writeToFile(file,data.toString());//o content vai vir aqui
				writer.append((CharSequence) write);
				writer.close();
			} catch (FileNotFoundException e1) {
				System.err.println(e1.getMessage());
				e1.printStackTrace();
			} catch (UnsupportedEncodingException e2) {
				System.err.println(e2.getMessage());
				e2.printStackTrace();
			}
			
			
			panel_score.add(text_area);
			frame_score.add(panel_score);
			frame_score.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
			frame_score.setSize(300,300);
			frame_score.setVisible(true);
		});
		bar = new JMenuBar();
		bar.add(file_Menu);
		
		//map
		panel.add(map,BorderLayout.CENTER);
		//
		new Timer(10, new ActionListener() {
			@Override
		    public void actionPerformed(ActionEvent e) {
				label_bombs.setText("Bombs remaining: " + map.get_qtd_bombs());
		    }
		}).start();
		label_bombs.setText("Bombs remaining: " + map.get_qtd_bombs());
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
	public int get_score(){
		return counter;
	}
	public String get_selected_difficult(){
		return selected_difficult;
	}

	//main
	public static void main(String[] args) {
		Interface window = new Interface();
	}
}