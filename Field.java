
public class Field {
	//this class is for an only camp
	//preciso implementar nessa classe o flood system
	//o bomb placement
	//how the click thingy works, theres the 3 ifs I have to do
	//gotta do the lose system too, maybe in another class?
	//i think I can merge de Camp class and the Map class
	
	private boolean have_bomb;
	
	public Field() {
		
	}
	
	public void set_bomb() {//esse set funciona..?
		have_bomb = true;		
	}
	public boolean have_bomb() {
		return have_bomb;
	}
	//method that returns how much bombs are near the area clicked
	public int bombs_near() {
		//TODO
		return 0;
	}
}
