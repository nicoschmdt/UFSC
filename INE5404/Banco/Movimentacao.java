
public class Movimentacao {
	private String descricao;
	private double valor;
	private String inf;
	
	public Movimentacao(){
		
	}
	public Movimentacao(String descricao, double valor, String inf){
		this.descricao=descricao;
		this.valor=valor;
		this.inf=inf;
	}
	public String getDescricao() {
		return descricao;
	}
	public void setDescricao(String descricao) {
		this.descricao = descricao;
	}
	public double getValor() {
		return valor;
	}
	public void setValor(double valor) {
		this.valor = valor;
	}
	public String getInf() {
		return inf;
	}
	public void setInf(String inf) {
		this.inf = inf;
	}
}