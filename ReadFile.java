import java.io.File;
import java.io.FileNotFoundException;
import java.util.NoSuchElementException;
import java.util.Scanner;

public class ReadFile {
	private Scanner input;
	
	public void openFile() {
		try {
			input = new Scanner(new File("score.txt"));
		}catch(FileNotFoundException e){
			System.err.println(e.getMessage());
			System.exit(1);
		}
	}
	public void read() {
		Score score = new Score();
		System.out.printf("%-s%-s%-d\n","Difficulty: ","Name","Time");
		try {
			while(input.hasNext()) {
				score.set_difficulty(input.next());
				score.set_name(input.next());
				score.set_time(input.nextInt());
			}
		}catch(NoSuchElementException e) {
			System.err.println(e.getMessage());
			input.close();
		}
	}public void closeFile() {
		if(input != null) {
			input.close();
		}
	}
}
