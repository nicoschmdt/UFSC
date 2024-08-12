public class Operacao {
	private int num1;
	private int num2;
	private double resultado;

	public Operacao(int num1, int num2) {
		this.num1 = num1;
		this.num2 = num2;
	}
	
	public Operacao() {
		this.num1 = 0;
		this.num2 = 0;
		this.resultado = 0;
	}

	void medPond(int num1, int num2, int p1, int p2) {
		this.resultado = ((num1*p1)+(num2*p2))/(p1+p2);
		return this.resultado;
		}

	 int calcFat(int num) {
		int temp = num;
		for(int i = num - 1; i > 0; i--) {
			temp = temp * i;
		}
		this.resultado = temp;
	}

	void subtrair() {
		this.resultado= this.num1 - this.num2;
	}
	
	double calcularPotencia() {
		int i= num2;
		double r=1;
		while(i>=1) {
			r*= num1;
			i--;
		}
		return this.resultado= r;
	}

	void soma() {
		this.resultado = this.num1 + this.num2;	
	}
	
	void calcularMedia(double num1, double num2) {
		this.resultado = (num1 + num2)/2;
	}
	
	double multiplicar() {
		return this.num1*this.num2;
	}
	
	double dividir(double dividendo, double divisor) {
		return dividendo/divisor;
	}
	
	public int getNum1() {
		return num1;
	}

	public void setNum1(int num1) {
		this.num1 = num1;
	}

	public int getNum2() {
		return num2;
	}

	public void setNum2(int num2) {
		this.num2 = num2;
	}

	public double getResultado() {
		return resultado;
	}

	public void setResultado(double resultado) {
		this.resultado = resultado;
	}
}
