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
	private int IB, IA,JB,JA;
	
	public Mouse(int i,int j,Field[][] f) {
		this.i = i;
		this.j = j;
		this.field = f;
		this.field_l = f.length;
		this.IB = i - 1;
		this.JB = j - 1;
		this.JA = j + 1;
		this.IA = i + 1;
	}
	public void mouseClicked(MouseEvent e) {
		
	}
	public void mousePressed(MouseEvent e) {
		JButton btn = (JButton) e.getSource();
		
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
						//HOW???
						
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

	public void flood_fill(Field field2, JButton btn) {
		
	}
}