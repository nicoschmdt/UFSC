public class Agencia {

    private int numero;
    private String nome;
    private String endereco;
    private Conta[] conta;
    private Cliente[] cliente;
    
    public Agencia() {
    	
    }
    public Agencia(int numero, String nome, String endereco, Conta[] conta, Cliente[] cliente) {
    	this.numero=numero;
    	this.nome=nome;
    	this.endereco=endereco;
    	this.conta=conta;
    	this.cliente=cliente;
    }
	public int getNumero() {
		return numero;
	}
	public void setNumero(int numero) {
		this.numero = numero;
	}
	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
	public String getEndereco() {
		return endereco;
	}
	public void setEndereco(String endereco) {
		this.endereco = endereco;
	}
	public Conta[] getConta() {
		return conta;
	}
	public void setConta(Conta[] conta) {
		this.conta = conta;
	}
	public Cliente[] getCliente() {
		return cliente;
	}
	public void setCliente(Cliente[] cliente) {
		this.cliente = cliente;
	}

}