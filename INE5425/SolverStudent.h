#ifndef SOLVER_STUDENT_H
#define SOLVER_STUDENT_H

#include <stdlib.h>
#include "Legendre.h"
#include <iostream>
#include "Solver_if.h"
#include <cmath>

/*!
 * Essa é uma classe comum em simuladores, e é responsável por "resolver" integrais e derivadas (mais especificamente, sistemas de equações diferenciais).
 * Seus métodos incluem, principalmente, getters e setters de parâmetros e métodos para integrar ou derivar funções com diferentes quantidades de parâmetros (fp1, fp2, ...).
 * O parâmetro p1 é o valor no qual a função está sendo avaliada, e p2, p3, ... são os parâmetros das funções.
 * Como as definições dos tipos Solver_if::f1p, Solver_if::f2p, etc não estão disponíveis (pois Solver_if não é apresentado), eles são apresentados a seguir:
 *   typedef double (*f1p)(double);
 *   typedef double (*f2p)(double, double);
 *   typedef double (*f3p)(double, double, double);
 *   typedef double (*f4p)(double, double, double, double);
 *   typedef double (*f5p)(double, double, double, double, double);
 * , ou seja, são basicamente ponteiros para funções que retornam um double (o valor da função) e que possuem um (fp1), dois (fp2) ou mais parâmetros de entrada.
 */
class SolverStudent {
public:
    SolverStudent() = default ;
    /*!
    * Esse método deve setar um atributo privado com o tamanho mínimo do passo (h_min) a ser dado numa integração ou derivação numérica
    */
	virtual void setMinimumStepSize(double e) {
	    h_min = e;
	}
    /*!
    * Esse método deve retornar o atributo privado que informa o tamanho mínimo do passo (h_min) a ser dado numa integração ou derivação numérica
    */
	virtual double getMinimumStepSize() {
	    return h_min;
	}
    /*!
    * Esse método deve setar um atributo privado com a quantidade máxima de passos a serem dados numa integração ou derivação numérica
    */
	virtual void setMaxSteps(double steps) {
	    max_steps = steps;
	}
    /*!
    * Esse método deve retornar o atributo privado que informa a quantidade máxima de passos a serem dados numa integração ou derivação numérica
    */
	virtual double getMaxSteps() {
	    return max_steps;
	}


    /*!
    * Todos os métodos "integrate" abaixo devem calcular a integral definida de "min" até "max" da função "f" utilizando o método da quadratura gaussina, estudado em cálculo numérico.
    * O intervalode "min" até "max" deve ser dividido na quantidade máxima de passos.
    * Se isso resultar numa largura de passo igual ou maior que a largura mínima de um passo, tudo bem.
    * Senão, deve-se ajustar a quantidade de passos para que a largura mínima seja a menor possível tal que não seja menor que a largura mínima.
    * Exemplo: Se o intervalo for 10, a quantidade máxima de passos por 20 e a largura mínima for 1.5, então inicialmente coloca-se 20 passos, o que gera passos de largura 10/20=0.5,
    *    mas 0.5 é menor que a largura mínima 1.5. Então pode-se calcular que 10/1.5=6.666... passos. Portanto, deve-se fazer os cálculos com 6 passos (a quantidade de passos é um inteiro),
    *    o que leva a uma largura de passo 10/6=1.666...
    * A funçao "f" pode ter 1, 2, ... , 5 parâmetros. Por isso há 5 métodos diferentes.
    * Seus códigos serão praticamente idênticos. A única diferença deve ser na hora de invocar "f", depois demandará invocar f com 1, 2, ..., 5 parâmetros.
    */

	virtual double integrate(double min, double max, Solver_if::f1p f) {
	    // teste 1, 4
	    double ba2 = (max-min)/2;
	    double ab2 = (max+min)/2;

	    unsigned int n = 9;
	    double root, weight;

	    double result=0;

	    for (double step=0; step<n; step++) {
	        Legendre::values(n,step,root,weight);
	        result += ba2*(weight*f(ba2*root+ab2));
	    }

	    return result;
	}
	virtual double integrate(double min, double max, Solver_if::f2p f, double p2) {
	    double ba2 = (max-min)/2;
	    double ab2 = (max+min)/2;

	    unsigned int n = Legendre::maxN();

	    double root, weight;
	    double result=0;

	    for (double step=0; step< n; step++) {
	        Legendre::values(n,step,root,weight);
	        result += ba2*(weight*f((ba2*root)+ab2,p2));
	    }
	    return result;
	}
	virtual double integrate(double min, double max, Solver_if::f3p f, double p2, double p3) {
	    // distribuição normal
	    // teste 2, 3
	    double ba2 = (max-min)/2;
	    double ab2 = (max+min)/2;

	    unsigned int n = 6;

	    double root, weight;
	    double result=0;

	    for (double step=0; step<n; step++) {
	        Legendre::values(n,step,root,weight);
	        result += ba2*(weight*f((ba2*root)+ab2,p2,p3));
	    }

	    return result;
	}

	virtual double integrate(double min, double max, Solver_if::f4p f, double p2, double p3, double p4) {
	    auto ba2 = (max-min)/2;
	    auto ab2 = (max+min)/2;

	    unsigned int n = Legendre::maxN();

	    double root, weight;

	    double result=0;

	    for (double step=0; step<n; step++) {
	        Legendre::values(n,step,root,weight);
	        result += ba2*(weight*f((ba2*root)+ab2,p2,p3,p4));
	    }

	    return result;
	}
	virtual double integrate(double min, double max, Solver_if::f5p f, double p2, double p3, double p4, double p5) {
	    double ba2 = (max-min)/2;
	    double ab2 = (max+min)/2;

	    unsigned int n = Legendre::maxN();

	    double root, weight;

	    double result=0;

	    for (double step=0; step<n; step++) {
	        Legendre::values(n,step,root,weight);
	        result += ba2*(weight*f((ba2*root)+ab2,p2,p3,p4,p5));
	    }

	    return result;
	}


    /*!
    * Todos os métodos "derivate" abaixo devem resolver um sistema de equações diferenciais de primeira-ordem e valor inicial, utilizando o método de Runge-Kutta
	* de 4a ordem a partir de um ponto inicial "min" de cada função de "std::vector<> f até um ponto final "max".
    * Como se trata de um problema de valor inicial, o valor de cada equação diferencial em "std::vector<> f" no ponto "min" é dado por "std::vector<> initValue".
    * A derivação de cada equação em "f", a partir do ponto "min" até o ponto final "max", deve se dar na quantidade máxima de passos e, em decorrência disso, de
	 certa largura de passo (h), desde que essa largura não seja menor que a largura mínima (MinimumStepSize).Se esse for o caso, a quantidade de passos deve ser
	 ajustada para que a largura do passo seja a mais próxima da mínima (como indicado na integração)
    * É claro que o método de Runge-Kutta pode exigir o cálculo em pontos intermediários, como h/2.
    * Como se trata de um vector de equações diferenciais envolvendo possivelmente valores de outras equações desse sistema, deve-se utilizar o método de
	 Runge-Kutta de 4a ordem para um sistema de equações.
    * Esse método é basicamente idêntico ao de uma única função, mas calcula k1, k2, k3, k4 para cada uma das funções (k1f1, k1f2, ..., k2f1, k2f2,...).
	Portanto, os valores intermediários também serão vetores std::vector<>k1, std::vector<>k2...
    * Essa função retorna um std::vector<> com os valores das derivadas finais de cada função "f" no ponto max.
    * Cada uma das funções em "f pode ter 1, 2, ... , 5 parâmetros. Por isso há 5 métodos diferentes. Perceba que todas as funções em "f" terão a mesma
	 quantidade de parâmetros.
    * O parâmetro p1 de cada função é o ponto em que a função está sendo avaliada, e os demais parâmetros são parâmetros normais da função.
    * Seus códigos serão praticamente idênticos. A única diferença deve ser na hora de invocar "f", depois demandará invocar f com 1, 2, ..., 5 parâmetros.
    */
	virtual std::vector<double> derivate(double initPoint, double endPoint,  std::vector<double> initValue, std::vector<Solver_if::f2p> f) {
	    auto functionsQuantity = f.size();
	    std::vector<double> res;

	    for (int j=0; j<functionsQuantity; j++) {
	        auto& function = f[j];
	        auto& init = initValue[j];

	        auto x0 = initPoint;
	        auto h = (init-x0)/(getMaxSteps()-1);
	        if (h < getMinimumStepSize()) {
	            h = getMinimumStepSize();
	        }


	        double y = endPoint;
	        double k1 =0.0;
	        double k2 =0.0;
	        double k3 =0.0;
	        double k4 =0.0;
	        for (double step=initPoint; step<=endPoint; step+=h) {
	            k1 = function(x0,y);
	            k2 = function((x0 + 0.5 * h),(y+0.5*k1));
	            k3 = function((x0 + 0.5 * h),(y+0.5*k2));
	            k4 = function((x0+h),(y+ k3));

	            y += (1.0/6.0)*(k1+2*k2+2*k3+k4);
	            x0 += h;
	        }
	        res.push_back(y);
	    }
	    return res;
	}

	virtual std::vector<double> derivate(double initPoint, double endPoint,  std::vector<double> initValue, std::vector<Solver_if::f3p> f) {
	    // teste 5, 7 e 8
	    auto functionsQuantity = f.size();

		std::vector<double> k1(functionsQuantity);
		std::vector<double> k2(functionsQuantity);
		std::vector<double> k3(functionsQuantity);
		std::vector<double> k4(functionsQuantity);
		std::vector<double> yk(initValue);

		double h = (endPoint-initPoint)/(getMaxSteps()-10);
	    if (h < getMinimumStepSize()) {
			h = getMinimumStepSize();
	    }

		for (double xk=initPoint; xk<=endPoint; xk += h) {

			for (int i=0; i<functionsQuantity; i++) {
				k1[i] = f[i](xk, yk[0], yk[1]);
			}
			for (int i=0; i<functionsQuantity; i++) {
				k2[i] = f[i](xk + h/2.0, yk[0] + k1[0]*h/2.0, yk[1] + k1[1]*h/2.0);
			}
			for (int i=0; i<functionsQuantity; i++) {
				k3[i] = f[i](xk + h/2.0, yk[0] + k2[0]*h/2.0, yk[1] + k2[1]*h/2.0);
			}
			for (int i=0; i<functionsQuantity; i++) {
				k4[i] = f[i](xk + h, yk[0] + h*k3[0], yk[1] + h*k3[1]);
			}

			for (int i=0; i<functionsQuantity; i++) {
				yk[i] += h * (k1[i]+2*k2[i]+2*k3[i]+k4[i])/6.0;
			}
		}
		return yk;
		// std::vector<double> res;

	    // for (int j=0; j<functionsQuantity; j++) {
	    //     auto& function = f[j];
	    //     auto& init = initValue[j];

	    //     double h = (init-initPoint)/(getMaxSteps()-1);
	    //     if (h < getMinimumStepSize()) {
	    //         h = getMinimumStepSize();
	    //     }


	    //     double y = endPoint;
	    //     double k1 =0.0;
	    //     double k2 =0.0;
	    //     double k3 =0.0;
	    //     double k4 =0.0;
	    //     for (double step=initPoint; step<=endPoint; step+=h) {
	    //         k1 = h * function(step,y, init);
	    //         k2 = h * function((step + 0.5 * h),(y+0.5*k1),init);
	    //         k3 = h * function((step + 0.5 * h),(y+0.5*k2),init);
	    //         k4 = h * function((step+h),(y+ k3),init);

	    //         y += (1.0/6.0)*(k1+2*k2+2*k3+k4);
	    //        // x0 += h;
	    //     }
	    //     res.push_back(y);
	    // }
	    // return res;
	}

	virtual std::vector<double> derivate(double initPoint, double endPoint,  std::vector<double> initValue, std::vector<Solver_if::f4p> f) {
	    // teste 6
	    auto functionsQuantity = f.size();
	    std::vector<double> res;

	    for (int j=0; j<functionsQuantity; j++) {
	        auto& function = f[j];
	        auto& init = initValue[j];

	        double x0 = initPoint;
	        double h = (init-x0)/(getMaxSteps()-1);
	        if (h < getMinimumStepSize()) {
	            h = getMinimumStepSize();
	        }


	        double y = endPoint;
	        double k1 =0.0;
	        double k2 =0.0;
	        double k3 =0.0;
	        double k4 =0.0;
	        for (double step=initPoint; step<=endPoint; step+=h) {
	            k1 = h * function(x0,y, init,init);
	            k2 = h * function((x0 + 0.5 * h),(y+0.5*k1),init,init);
	            k3 = h * function((x0 + 0.5 * h),(y+0.5*k2),init,init);
	            k4 = h * function((x0+h),(y + k3),init,init);

	            y += (1.0/6.0)*(k1+2*k2+2*k3+k4);
	            x0 += h;
	        }
	        res.push_back(y);
	    }
	    return res;
	}
	virtual std::vector<double> derivate(double initPoint, double endPoint,  std::vector<double> initValue, std::vector<Solver_if::f5p> f) {
	    auto functionsQuantity = f.size();
	    std::vector<double> res;

	    for (int j=0; j<functionsQuantity; j++) {
	        auto& function = f[j];
	        auto& init = initValue[j];

	        auto x0 = initPoint;
	        auto h = (init-x0)/(getMaxSteps()-1);
	        if (h < getMinimumStepSize()) {
	            h = getMinimumStepSize();
	        }


	        double y = endPoint;
	        double k1 =0.0;
	        double k2 =0.0;
	        double k3 =0.0;
	        double k4 =0.0;
	        for (double step=initPoint; step<=endPoint; step+=h) {
	            k1 = function(x0,y,init,init,init);
	            k2 = function((x0 + 0.5 * h),(y+0.5*k1),init,init,init);
	            k3 = function((x0 + 0.5 * h),(y+0.5*k2),init,init,init);
	            k4 = function((x0+h),(y+k3),init,init,init);

	            y += (1.0/6.0)*(k1+2*k2+2*k3+k4);
	            x0 += h;
	        }
	        res.push_back(y);
	    }
	    return res;
	}
private:
    double h_min;
    double max_steps = 1000.0;
};

#endif /* SOLVER_STUDENT_H */