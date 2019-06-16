
public class Field {
	//this class is for an only camp
	//preciso implementar nessa classe o flood system
	//how the click thingy works, theres the 3 ifs I have to do
	//gotta do the lose system too, maybe in another class?
	
	private boolean have_bomb;
	private boolean have_number;
	private int number;
	
	public Field() {
		have_bomb = false;
	}
	
	public void set_bomb() {//esse set funciona..?
		have_bomb = true;		
	}
	public boolean have_bomb() {
		return have_bomb;
	}
	public void set_number() {
		have_number = true;
	}
	public boolean have_number() {
		return have_number;
	}
	public void set_number(int n) {
		number = n;
	}
	public int get_number() {
		return number;
	}
	//method that returns how much bombs are near the area clicked
	public int bombs_near() {
		//TODO
		return 0;
	}
}
