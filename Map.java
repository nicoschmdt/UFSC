import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import javax.swing.JButton;
import javax.swing.JPanel;

public class Map extends JPanel implements ActionListener{
	
	private Field[][] field; //this is the matrix he'll go to confirm whats going on
	private JButton[][] buttons; //the clickable part of the minesweeper
	//the next variables follow the order of easy -> medium -> hard kind of setup.
	//still idk how to connect those two parts :(
	private int[] quantity_of_bombs = {10,40,100};
	private int[] size_of_map = {10,18,24};
	private GridBagConstraints constraints;
	private GridBagLayout grid_layout;
	private Random random;
	private int column;
	private int line;
	//the number of the position to get with the level chosen
	private int level = 0;

	public Map() {
//		super();
		int var_size = size_of_map[0];
		//
		field = new Field[size_of_map[level]][size_of_map[level]];
		
		buttons = new JButton[size_of_map[level]][size_of_map[level]];
		//inicializando o objeto constraints
		
		grid_layout = new GridBagLayout();
		setLayout(grid_layout);
		
		constraints = new GridBagConstraints();
		constraints.fill = GridBagConstraints.BOTH;
		
		for(int i = 0; i < var_size ; i++) {
			for(int j = 0; j < var_size; j++) {
				buttons[i][j] = new JButton("");
				//
				buttons[i][j].setPreferredSize(new Dimension(25,25));
				buttons[i][j].setBackground(new Color(205,200,177));
				addComponent(buttons[i][j],i+1,j,1,1);

				//actionListener
				buttons[i][j].addActionListener(this);			
			}
		}
		
	}
	public void get_difficulty(String s) {
		if(s.equals("Easy")) {
			level = 0;
		}else if(s.equals("Medium")) {
			level = 1;
		}else {
			level = 2;
		}
		
	}
	public void sort_bomb_placement(JButton[][] jb,int size_of_matrix) {
		//gotta generalize this
		random = new Random();
		//this way it'll choose an aleatory place in the matrix
		column = random.nextInt(size_of_matrix); 
		line = random.nextInt(size_of_matrix);
		for(int i = 0; i < quantity_of_bombs[level]; i++) {
			column = random.nextInt(); 
			line = random.nextInt();
			if(field[line][column].have_bomb()) {
				i--;
			}else {
				field[line][column].set_bomb();
			}
			
		}
	}
	
	private void addComponent(Component component, int row, int column, int width, int height) {
		constraints.gridx = column;
		constraints.gridwidth = width;
		constraints.gridy = row;
		constraints.gridheight = height;
		grid_layout.setConstraints(component, constraints);
		add(component);
		
	}
	@Override
	public void actionPerformed(ActionEvent e) {
		JButton btn = (JButton) e.getSource();
//		if(buttons[pos_i][pos_j] == (JButton)e.getSource()) {
			btn.setEnabled(false);
			btn.setBackground(new Color(205,179,139));
//		}
		//verify if there's a bomb and then decide what is going to happen
//		buttons[i][j].setBackground(new Color(205,179,139));
//		buttons[i][j].setEnabled(false);
	}
}
