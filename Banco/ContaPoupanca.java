public class ContaPoupanca extends Conta {
	private int variacao;
	private double rendimento_mensal;
	public ContaPoupanca(){
		
	}
	public ContaPoupanca(int numero, double saldo, double limite_saque, Movimentacao movimentacoes[], int variacao, double rendimento_mensal){
		super(numero, saldo, limite_saque, movimentacoes);
		this.variacao=variacao;
		this.rendimento_mensal=rendimento_mensal;
	}
	public int getVariacao() {
		return variacao;
	}
	public void setVariacao(int variacao) {
		this.variacao = variacao;
	}
	public double getRendimento_mensal() {
		return rendimento_mensal;
	}
	public void setRendimento_mensal(double rendimento_mensal) {
		this.rendimento_mensal = rendimento_mensal;
	}
}
