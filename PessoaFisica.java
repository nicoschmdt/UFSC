public class PessoaFisica extends Cliente {
    private int cpf;
    private String estadoCivil;

    public PessoaFisica() {

    }

    public PessoaFisica(int cpf, String estadoCivil) {
        this.cpf = cpf;
        this.estadoCivil = estadoCivil;
    }

    public void setCPF(int cpf) {
        this.cpf = cpf;
    }
    public int getCPF() {
        return this.cpf;
    }
    public void setEstadoCivil(String estadoCivil) {
        this.estadoCivil;
    }
    public String getEstadoCivil() {
        return this.estadoCivil;
    }



}