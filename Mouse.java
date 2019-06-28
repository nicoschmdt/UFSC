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
		System.out.println(map);
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
						//fazer metodo floodfill aq
						flood_fill(i,j);
						
					}
				}else {//if there's a bomb
					System.out.println("Oh no, you lost the game! <('^')> ");
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
				}else {
					btn.setEnabled(false);
					btn.setText("X");
					field[i][j].set_have_flag(true);
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
		//Im having problem when I call the method once again
		int IB = a - 1; // i before
		int JB = b - 1; // j before
		int JA = b + 1; // j after
		int IA = a + 1; // i after
		if(IB>=0) {
			if(field[IB][j].have_number()) {
				buttons[IB][j].setText(Integer.toString(field[IB][j].get_number()));
				buttons[IB][j].setEnabled(false);
				buttons[IB][j].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IB,j);
			}
		}
		if(IB>=0 && JB>=0) {
			if(field[IB][JB].have_number()) {
				buttons[IB][JB].setText(Integer.toString(field[IB][JB].get_number()));
				buttons[IB][JB].setEnabled(false);
				buttons[IB][JB].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IB,JB);
			}
		}
		if(JB>=0) {
			if(field[i][JB].have_number()) {
				buttons[i][JB].setText(Integer.toString(field[i][JB].get_number()));
				buttons[i][JB].setEnabled(false);
				buttons[i][JB].setBackground(new Color(205,179,139));
			}else {
				flood_fill(i,JB);
			}
		}
		if(IB>=0 && JA<buttons.length) {
			if(field[IB][JA].have_number()) {
				buttons[IB][JA].setText(Integer.toString(field[IB][JA].get_number()));
				buttons[IB][JA].setEnabled(false);
				buttons[IB][JA].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IB,JA);
			}
		}
		if(JA<buttons.length) {
			if(field[i][JA].have_number()) {
				buttons[i][JA].setText(Integer.toString(field[i][JA].get_number()));
				buttons[i][JA].setEnabled(false);
				buttons[i][JA].setBackground(new Color(205,179,139));
			}else {
				flood_fill(i,JA);
			}
		}
		if(JB>=0 && IA<buttons.length) {
			if(field[IA][JB].have_number()) {
				buttons[IA][JB].setText(Integer.toString(field[IA][JB].get_number()));
				buttons[IA][JB].setEnabled(false);
				buttons[IA][JB].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IA,JB);
			}
		}
		if(IA<buttons.length) {
			if(field[IA][j].have_number()) {
				buttons[IA][j].setText(Integer.toString(field[IA][j].get_number()));
				buttons[IA][j].setEnabled(false);
				buttons[IA][j].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IA,j);
			}
		}
		if(IA <buttons.length && JA<buttons.length) {
			if(field[IA][JA].have_number()) {
				buttons[IA][JA].setText(Integer.toString(field[IA][JA].get_number()));
				buttons[IA][JA].setEnabled(false);
				buttons[IA][JA].setBackground(new Color(205,179,139));
			}else {
				flood_fill(IA,JA);
			}
		}
	}
}