import java.util.Scanner;
public class Banco {
	Scanner ler= new Scanner(System.in);
	private Conta[] array = new Conta[20];
	private Movimentacao[] movimentacoes= new Movimentacao[10];
	private int i;
	private Cliente[] clientes= new Cliente[20];
	private Agencia[] agencias= new Agencia[5];
	
	public Banco() {
		
	}
	public Banco(Conta[] array, int i){
		this.array=array;
		this.i=0;
	}
	
	public Conta new_Conta(int tipo){
		if(array[i]!=null) {
			i++;
		}else
			
		if(tipo==1){
			ContaPoupanca poupanca = new ContaPoupanca();
			poupanca.setNumero(i);
			System.out.println("insira o saldo da conta: ");
			int x = ler.nextInt();
			poupanca.setSaldo(x);
			System.out.println("insira a variação: ");
			x = ler.nextInt();
			poupanca.setVariacao(x);
			System.out.println("insira o rendimento mensal: ");
			x = ler.nextInt();
			poupanca.setRendimento_mensal(x);
			array[i]= poupanca;
			i++;
		}else
			if(tipo==2){
				ContaCorrente corrente = new ContaCorrente();
				corrente.setNumero(i);
				System.out.println("insira o saldo da conta: ");
				int y = ler.nextInt();
				corrente.setSaldo(y);
				System.out.println("possui cheque especial? S ou N ");
				String z= ler.next();
						if(z.equals("S")||z.equals("s")) {
							corrente.setStatus(true);
							System.out.println("qual o limite do cheque especial? ");
							y= ler.nextInt();
							corrente.setLimite_ce(y);
						}else
							if(z.equals("N")||z.equals("n")) {
								corrente.setStatus(false);
							}
				array[i]= corrente;
				i++;
			}
		return array[i];
	}
	public void delete_Conta(int numero) {
		array[numero]= new Conta();
	}
	public void sacar(int tipo, int numero, double valor) {
		Movimentacao x= new Movimentacao();
		String desc= ler.next();
		x.setDescricao(desc);
		x.setInf("saque");
		x.setValor(valor);
		int i=0;
		movimentacoes[i]=x;
		i++;
		double lim= array[numero].getLimite_saque();
		double saldo = array[numero].getSaldo();
		if(tipo==1) {
		if(saldo<valor) {
			System.out.println("saldo insuficiente");
		} else
			if(valor>lim) {
				System.out.println("valor excedo o limite de saque");
			}
		}
		else
			if(tipo==2) {
				for(Conta c: array) {
					if( c instanceof ContaCorrente) {
						if(((ContaCorrente)c).isStatus()) {		
							lim += ((ContaCorrente)c).getLimite_ce();
						}
					}
				}
				if(saldo<valor) {
					System.out.println("saldo insuficiente");
				} else
					if(valor>lim) {
						System.out.println("valor excedo o limite de saque");
					}
				}
		double res= saldo- valor;
		array[numero].setSaldo(res);
		movimentacoes[i].setInf("saque");
		array[numero].setMovimentacoes(movimentacoes);
	}
}
