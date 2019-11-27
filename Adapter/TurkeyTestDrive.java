
public class TurkeyTestDrive {
	public static void main(String[] args) {
		WildTurkey turkey = new WildTurkey();
		
		MallardDuck duck = new MallardDuck();
		Turkey duckAdapter = new DuckAdapter(duck);
		
		System.out.println("The Turkey says...");
		turkey.gobble();
		for(int i = 0; i < 5; i++) {
			turkey.fly();
		}
		
		System.out.println("The Duck says...");
		duck.quack();
		duck.fly();
		
		System.out.println("The DuckAdapter says...");
		duckAdapter.gobble();
		duckAdapter.fly();
	}
	
	static void testTurkey(Turkey turkey){
		turkey.gobble();
		turkey.fly();
	}
}
