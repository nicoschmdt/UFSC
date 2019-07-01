import java.awt.Color;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import javax.swing.JButton;
import javax.swing.SwingUtilities;

public class Mouse implements MouseListener{
	private int i;
	private int j;
	private Field[][] field;
	private Map map;
	private int field_l;
	private JButton[][] buttons;
	
	public Mouse(int i,int j,Field[][] f,Map map) {
		this.i = i;
		this.j = j;
		this.field = f;
		this.field_l = f.length;
		this.map = map;
		
	}
	public void mouseClicked(MouseEvent e) {
		
	}
	public void mousePressed(MouseEvent e) {
		JButton btn = (JButton) e.getSource();
		buttons = map.get_buttons();
//		System.out.println(f.get_flag());
		if(SwingUtilities.isLeftMouseButton(e)) {
			if(!field[i][j].get_flag()) {
				btn.setEnabled(false);
				
				btn.setBackground(new Color(205,179,139));
				field[i][j].set_click();
				if(!field[i][j].have_bomb()) {
					if(field[i][j].have_number()) {
						btn.setText(Integer.toString(field[i][j].get_number()));
					}else { //if there's nothing
						flood_fill(i,j);
						
					}
				}else if(field[i][j].have_bomb()){//if there's a bomb
//					System.out.println("Oh no, you lost the game! <('^')> ");
					for(int a = 0; a < buttons.length; a++) {
						for(int b = 0; b < buttons.length; b++) {
							buttons[a][b].setEnabled(false);
							if(field[a][b].have_bomb()) {
								buttons[a][b].setBackground(new Color(121, 255, 77));
							}
						}
					}
					//JK, still working on this.
				}
			}
		}else if(SwingUtilities.isMiddleMouseButton(e)) {
			
		}else {
//			btn.setBackground(new Color(205,200,177));
			if(!field[i][j].get_click()) {
				if(field[i][j].get_flag()) {
					btn.setEnabled(true);
					btn.setText("");
					field[i][j].set_have_flag(false);
					map.plus_one();
					
				}else {
					btn.setEnabled(false);
					btn.setText("X");
					field[i][j].set_have_flag(true);
					map.minus_one();
				}
			}
			//gotta see a way to bring that content here	
			
		}
	}
	@Override
	public void mouseReleased(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}
	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub
		
	}

	public void flood_fill(int a,int b) {
		int IB = a - 1; // i before
		int JB = b - 1; // j before
		int JA = b + 1; // j after
		int IA = a + 1; // i after
		if(!field[a][b].have_number()) {
			buttons[a][b].setEnabled(false);
			buttons[a][b].setBackground(new Color(205,179,139));
		}
		if(IB>=0) {
			if(field[IB][b].have_number()) {
				buttons[IB][b].setText(Integer.toString(field[IB][b].get_number()));
				buttons[IB][b].setEnabled(false);
				buttons[IB][b].setBackground(new Color(205,179,139));
			}else if(buttons[IB][b].isEnabled() && !field[IB][b].have_bomb() && !field[IB][b].have_number()){
				flood_fill(IB,b);
			}
		}
		if(IB>=0 && JB>=0) {
			if(field[IB][JB].have_number() ) {
				buttons[IB][JB].setText(Integer.toString(field[IB][JB].get_number()));
				buttons[IB][JB].setEnabled(false);
				buttons[IB][JB].setBackground(new Color(205,179,139));
			}else if(buttons[IB][JB].isEnabled() && !field[IB][JB].have_bomb() && !field[IB][JB].have_number()) {
				flood_fill(IB,JB);
			}
		}
		if(JB>=0) {
			if(field[a][JB].have_number()) {
				buttons[a][JB].setText(Integer.toString(field[a][JB].get_number()));
				buttons[a][JB].setEnabled(false);
				buttons[a][JB].setBackground(new Color(205,179,139));
			}else if(buttons[a][JB].isEnabled() && !field[a][JB].have_bomb() && !field[a][JB].have_number()){
				flood_fill(a,JB);
			}
		}
		if(IB>=0 && JA<buttons.length) {
			if(field[IB][JA].have_number()) {
				buttons[IB][JA].setText(Integer.toString(field[IB][JA].get_number()));
				buttons[IB][JA].setEnabled(false);
				buttons[IB][JA].setBackground(new Color(205,179,139));
			}else if(buttons[IB][JA].isEnabled() && !field[IB][JA].have_bomb() && !field[IB][JA].have_number()){
				flood_fill(IB,JA);
			}
		}
		if(JA<buttons.length) {
			if(field[a][JA].have_number()) {
				buttons[a][JA].setText(Integer.toString(field[a][JA].get_number()));
				buttons[a][JA].setEnabled(false);
				buttons[a][JA].setBackground(new Color(205,179,139));
			}else if(buttons[a][JA].isEnabled() && !field[a][JA].have_bomb() && !field[a][JA].have_number()){
				flood_fill(a,JA);
			}
		}
		if(JB>=0 && IA<buttons.length) {
			if(field[IA][JB].have_number()) {
				buttons[IA][JB].setText(Integer.toString(field[IA][JB].get_number()));
				buttons[IA][JB].setEnabled(false);
				buttons[IA][JB].setBackground(new Color(205,179,139));
			}else if(buttons[IA][JB].isEnabled() && !field[IA][JB].have_bomb() && !field[IA][JB].have_number()){
				flood_fill(IA,JB);
			}
		}
		if(IA<buttons.length) {
			if(field[IA][b].have_number()) {
				buttons[IA][b].setText(Integer.toString(field[IA][b].get_number()));
				buttons[IA][b].setEnabled(false);
				buttons[IA][b].setBackground(new Color(205,179,139));
			}else if(buttons[IA][b].isEnabled() && !field[IA][b].have_bomb() && !field[IA][b].have_number()){
				flood_fill(IA,b);
			}
		}
		if(IA <buttons.length && JA<buttons.length) {
			if(field[IA][JA].have_number()) {
				buttons[IA][JA].setText(Integer.toString(field[IA][JA].get_number()));
				buttons[IA][JA].setEnabled(false);
				buttons[IA][JA].setBackground(new Color(205,179,139));
			}else if(buttons[IA][JA].isEnabled() && !field[IA][JA].have_bomb() && !field[IA][JA].have_number()){
				flood_fill(IA,JA);
			}
		}
	}
}