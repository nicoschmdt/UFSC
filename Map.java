import java.awt.Component;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JPanel;

public class Map extends JPanel {
	
	private JButton[][] buttons; //the clickable part of the minesweeper
	//the next variables follow the order of easy -> medium -> hard kind of setup.
	//still idk how to connect those two parts :(
	private int[] quantity_of_bombs = {10,40,100};
	private int[] size_of_map = {10,18,24};
	private int[] quantity_of_buttons = {100,324,576};
	private GridBagConstraints constraints;
	private GridBagLayout grid_layout;
	private int choose_quantity; // this is the quantity of buttons in the map
	
	
	public Map() {
//		super();
		int var_size = size_of_map[0];
		 // gotta generalize this but for the test I'm letting it this way
		//if pois o tamanho depende da dificuldade, deixarei sem o if por enquanto
		
		
		buttons = new JButton[10][10];
		//inicializando o objeto constraints
		
		grid_layout = new GridBagLayout();
		setLayout(grid_layout);
		
		constraints = new GridBagConstraints();
		constraints.fill = GridBagConstraints.BOTH;
		
		for(int i = 0; i < var_size ; i++) {
			for(int j = 0; j < var_size; j++) {
				buttons[i][j] = new JButton("");
				addComponent(buttons[i][j],i+1,j,1,1);
				
			}
		}
		//ACTIONLISTENER
		for(int i = 0; i < var_size ; i++) {
			for(int j = 0; j < var_size; j++) {
				buttons[i][j].addActionListener(new ActionListener() {
					
					@Override
					public void actionPerformed(ActionEvent e) {
						//TODO
						//verify if there's a bomb and then decide what is going to happen
						
					}
				});
			
			}
		}
		
	}
	public int choose_quantity(int n) {
		
		if(n == 10) {
			return  quantity_of_buttons[0];
		}else if(n == 18) {
			return  quantity_of_buttons[1];
		}else {
			return quantity_of_buttons[2];
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
}
