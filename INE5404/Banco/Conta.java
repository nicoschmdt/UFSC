public class Conta {
	private int numero;
	private double saldo;
	private double limite_saque;
	private Movimentacao movimentacoes[];
	
	public Conta(){
		
	}
	public Conta(int numero, double saldo, double limite_saque, Movimentacao movimentacoes[]){
		this.numero= numero;
		this.saldo= 0;
		this.limite_saque= 2000;
		this.movimentacoes=movimentacoes;
	}
	public Movimentacao[] getMovimentacoes() {
		return movimentacoes;
	}
	public void setMovimentacoes(Movimentacao[] movimentacoes) {
		this.movimentacoes = movimentacoes;
	}
	public int getNumero() {
		return numero;
	}
	public void setNumero(int numero) {
		this.numero = numero;
	}
	public double getSaldo() {
		return saldo;
	}
	public void setSaldo(double saldo) {
		this.saldo = saldo;
	}
	public double getLimite_saque() {
		return limite_saque;
	}
	public void setLimite_saque(double limite_saque) {
		this.limite_saque = limite_saque;
	}

}
