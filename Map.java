import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.util.Random;
import javax.swing.JButton;
import javax.swing.JPanel;

public class Map extends JPanel{
	
	private Field[][] field; //this is the matrix he'll go to confirm whats going on
	private JButton[][] buttons;
	//the next variables follow the order of easy -> medium -> hard setup.
	private int[] quantity_of_bombs = {20,70,200};
	private int[] size_of_map = {10,18,24};
	private GridBagConstraints constraints;
	private GridBagLayout grid_layout;
	private Random random;
	private int column;
	private int line;
	private Mouse mouse;
	//the number of the position to get with the level chosen
	private int level;
	private int comparison;
	private int bombs_map;
	private boolean game_lost = false;
	private boolean game_won = false;
	
	public Map(int level) {
		
		this.level = level;
		resize();
		bombs_map = quantity_of_bombs[level];
		comparison = quantity_of_bombs[level];
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
//					buttons[i][j].setBackground(new Color(000,178,238));
				}
				//actionListener
				
				mouse = new Mouse(i,j,field,this);
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
	public JButton[][] get_buttons(){
		return this.buttons;
	}
	public int get_qtd_bombs(){
		return bombs_map;
	}
	public void minus_one() {
		if(bombs_map>0) {
			bombs_map = bombs_map - 1;
		}
	}
	public void plus_one() {
		if(bombs_map< comparison) {
			bombs_map = bombs_map + 1;
		}
	}
	public void set_game_lost(boolean b) {
		this.game_lost = b;
	}
	public boolean get_game_lost() {
		return this.game_lost;
	}
	public void set_game_won(boolean b) {
		this.game_won = b;
	}
	public boolean get_game_won() {
		return this.game_won;
	}
	public void set_numbers(Field[][] f) {// here it'll be setted the quantity of numbers
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
				if(!f[i][j].have_bomb()) {

					
					if(ICM >= 0) {
						if(f[ICM][j].have_bomb()) {
							counter++;
						}
					}
					if(ICP< f.length) {
						if(f[ICP][j].have_bomb()) {
							counter++;
						}
					}
					if(JCM >= 0) {
						if(f[i][JCM].have_bomb()) {
							counter++;
						}
					}
					if(JCP < f.length) {
						if(f[i][JCP].have_bomb()) {
							counter++;
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
				if(counter == 0) {
					
				}else {
					f[i][j].set_number(counter);
					f[i][j].set_number();
				}
			}
		}
		
	}
}