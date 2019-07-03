import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.Formatter;
import java.util.Scanner;

public class WriteFile {
	
	private String path;
	
	public WriteFile() {
		
	}
	public void writeToFile(File f,String line) {
		FileWriter write;
		try {
			write = new FileWriter(f);
			PrintWriter printer = new PrintWriter(write);
			printer.printf("%s" + "%n", line);
			printer.close();
		} catch (IOException e) {
			System.err.println(e.getMessage());
			e.printStackTrace();
		}
	}
	
	
//    private Formatter output;
//    public WriteFile() {
//    	try {
//			output = new Formatter("score.txt");
//		} catch (FileNotFoundException e) {
//			System.err.println(e.getMessage());
//			e.printStackTrace();
//		}catch(SecurityException e) {
//			System.err.println(e.getMessage());
//			e.printStackTrace();
//			System.exit(1);
//		}
//    }
//    public void addRecords(Interface i) {
//        Score score = new Score();
//        Scanner input = new Scanner(System.in); //get the name here
//        int score_value = i.get_score();
//        score.set_name(input.next());
//        String difficulty = i.get_selected_difficult();
//
//        if(score.get_time() > 0) {
//            output.format("%s %s %d\n", difficulty,score.get_name(),score_value);
//        }else{
//            System.out.println("Time must be greater than 0.");
//        }
//    }
//    public void close_file() {
//        if(output != null) {
//            output.close();
//        }
//    }
}
