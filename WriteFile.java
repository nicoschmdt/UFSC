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
	
	

}