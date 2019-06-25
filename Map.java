import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Random;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;

public class Map extends JPanel{
	
	private Field[][] field; //this is the matrix he'll go to confirm whats going on
	private JButton[][] buttons;
	//the next variables follow the order of easy -> medium -> hard kind of setup.
	//still idk how to connect those two parts :(
	private int[] quantity_of_bombs = {35,95,200};
	private int[] size_of_map = {10,18,24};
	private GridBagConstraints constraints;
	private GridBagLayout grid_layout;
	private Random random;
	private int column;
	private int line;
	//the number of the position to get with the level chosen
	private int level;
	private int comparison;
//	private boolean have_flag;
//	private boolean is_clicked;//p

	public Map(int level) {
		this.level = level;
		resize();
	}
	public void resize() {
		int var_size = size_of_map[level];
		field = new Field[var_size][var_size];
		for(int i = 0; i < var_size; i ++) {
			for(int j = 0; j < var_size; j ++) {
				field[i][j] = new Field();
			}
		}
		//now the map has bombs
		sort_bomb_placement(buttons,size_of_map[level]);
		set_numbers(field);
		buttons = new JButton[var_size][var_size];
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
				buttons[i][j].setMargin(new Insets(5,5,5,5)); // this way the X appears
				addComponent(buttons[i][j],i+1,j,1,1);
				//test so I can see where the bombs are
				if(field[i][j].have_bomb()) {
					buttons[i][j].setBackground(new Color(000,178,238));
				}
				//actionListener
				Mouse mouse = new Mouse(i,j,field);
				buttons[i][j].addMouseListener(mouse);
			}
		}
	}

	public void sort_bomb_placement(JButton[][] jb,int size_of_matrix) {
		
		random = new Random();
		//this way it'll choose an aleatory place in the matrix
		for(int i = 0; i < quantity_of_bombs[level]; i++) {
			column = random.nextInt(size_of_matrix);
			line = random.nextInt(size_of_matrix);
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
	

	public void flood_fill(Field f) { //heres going to be the flood fill
		if(f.have_bomb()) {
			
		}else {
			if(f.have_number()) {
				
			}else {
				
			}
		}
	}

	
	public void set_numbers(Field[][] f) {// here it'll be setted the quantity of numbers, smtw it looks a little like the method above
		int ICM;//i counter minus
		int JCM;//j counter minus
		int ICP;//i counter plus
		int JCP;//j counter plus
		int counter = 0;
		for(int i = 0; i < f.length; i++ ) {
			for(int j = 0; j < f.length; j++) {
				
				counter = 0;
				ICM = i - 1;
				JCM = j - 1;
				ICP = i+1;
				JCP = j+1;
				if(!f[i][j].have_bomb()) {//this if is working

					if(f[i][j].have_bomb()) {
						counter++;
					}
					if(ICM >= 0) {
						if(f[ICM][j].have_bomb()) {
							counter++;
						}
						if(ICP< f.length ) {
							if(f[ICP][j].have_bomb()) {
								counter++;
							}
						}
					}
					if(JCM >= 0) {
						if(f[i][JCM].have_bomb()) {
							counter++;
						}
						if(JCP < f.length) {
							if(f[i][JCP].have_bomb()) {
								counter++;
							}
						}
					}
					if(ICM >= 0 && JCM >= 0 ) {
						if(f[ICM][JCM].have_bomb()) {
							counter++;
						}
					}
					if(JCP < f.length && ICP < f.length) {
						if(f[ICP][JCP].have_bomb()) {
							counter++;
						}
					}
					if(ICM >= 0 && JCP < f.length) {
						if(f[ICM][JCP].have_bomb()) {
							counter++;
						}
					}
					if(ICP < f.length && JCM >= 0) {
						if(f[ICP][JCM].have_bomb()) {
							counter++;
						}
					}
				}
				f[i][j].set_number(counter);
			}
		}
		
	}
}