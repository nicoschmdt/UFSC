
public class Field {
	//this class is for an only camp	
	private boolean have_bomb;
	private boolean have_number;
	private int number;
	private boolean have_flag;
	private boolean is_clicked;
	
	public Field() {
		have_bomb = false;
		have_flag = false;
		is_clicked = false;
	}
	
	public void set_bomb() {
		this.have_bomb = true;	
	}
	public boolean have_bomb() {
		return this.have_bomb;
	}
	public void set_number() {
		this.have_number = true;
	}
	public boolean have_number() {
		return this.have_number;
	}
	public void set_number(int n) {
		this.number = n;
	}
	public int get_number() {
		return this.number;
	}
	public void set_have_flag(boolean f) {
		this.have_flag = f;
	}
	public boolean get_flag() {
		return this.have_flag;
	}
	public void set_click() {
		this.is_clicked = true;
	}
	public boolean get_click() {
		return this.is_clicked;
	}
}