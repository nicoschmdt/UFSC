import java.util.Scanner;
public class Main {
	public static void main(String[] args) {
	int tipo;
	Banco b= new Banco();
	Scanner ler= new Scanner(System.in);
	System.out.println("Menu:\n1- Criar conta\n2- Excluir conta\n3- Sacar\n4- Sair");
	int opcao = ler.nextInt();
	switch(opcao) {
	case 1:
		System.out.println("Deseja criar uma conta do tipo poupança ou do tipo corrente?\n1: conta poupança\n2: conta poupança");
		tipo= ler.nextInt();
		b.new_Conta(tipo);
	case 2: 
		System.out.println("Qual o numero da conta que deseja excluir?");
		int n= ler.nextInt();
		b.delete_Conta(n);
	case 3: 
		System.out.println("Qual e o tipo da conta?");
		tipo= ler.nextInt();
		System.out.println("Qual e o numero da conta?");
		int num= ler.nextInt();
		System.out.println("Qual seria o valor a ser sacado?");
		double valor= ler.nextDouble();
		b.sacar(tipo, num, valor);
	case 4:
		break;
		
	}
	}
	    
}
