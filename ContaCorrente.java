public class ContaCorrente extends Conta {
	private boolean status;
	private double limite_ce; 
	public ContaCorrente(){
		
	}
	public ContaCorrente(int numero, double saldo, Movimentacao movimentacoes[], double limite_saque, boolean status, double limite_ce){
		super(numero, saldo, limite_saque, movimentacoes);
		this.status=status;
		this.limite_ce=limite_ce;
	}
	public boolean isStatus() {
		return status;
	}
	public void setStatus(boolean status) {
		this.status = status;
	}
	public double getLimite_ce() {
		return limite_ce;
	}
	public void setLimite_ce(double limite_ce) {
		this.limite_ce = limite_ce;
	}

}
