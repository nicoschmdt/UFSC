
#ifndef PROBABILITYDISTRIBUTIONSTUDENT_H
#define PROBABILITYDISTRIBUTIONSTUDENT_H

#include "ProbabilityDistributionBase.h"
#include "PDProxy.h"
#include "SolverProxy.h"
#include <cstddef>
#include <math.h>
#include <stdlib.h>
#include <iostream>
#include <tuple>

struct normalDistributionCacheEntry {
    double mean;
    double stddev;
    double a;
    double b;
    double cumulativeProbability;
};

struct tDistributionCacheEntry {
    double degreeFreedom;
    double a;
    double b;
    double cumulativeProbability;
};

std::vector<normalDistributionCacheEntry> normalDistributionCache;
std::vector<tDistributionCacheEntry> tDistributionCache;

bool isClose(double val1, double val2) {
    return std::abs(val1 - val2) <= 1e-16;
}

void insertInNormalCache(normalDistributionCacheEntry value) {
    for (normalDistributionCacheEntry cachedValue : normalDistributionCache) {
        if (isClose(cachedValue.mean,value.mean) && isClose(cachedValue.stddev, value.stddev) && isClose(cachedValue.a, value.a) && isClose(cachedValue.b, value.b)) {
            return;
        }
    }
    normalDistributionCache.push_back(value);
}

/*!
* Essa classe deve encontrar o valor x de uma distribuição de probabildiade cuja probabilidade acumulada corresponda a um valor dado.
* Vamos inicialmente ver o caso comum, que é achar o valor da probabildiade acumulada de uma distribuição até o valor x dado.
* Por exemplo, para encontrar o valor da probabilidade acumulada até o valor x=1.5 numa dsitrbuição de probabilidade normal padrão (com média 0 e desvio-padrão 1),
   podemos simplesmente calcular a integral definida de -infinito até 1.5. Como "-infinito" não existe numericamente, poderíamos simplesmente colocar o menor número real representável.
* Porém, podemos tirar proveito de conhecimentos da disciplina de probabilidade e estatística e saber que praticamente 100% da área de uma distribuição de probabilidade está entre
   a média - 4xdesvio e média + 4xdesvio. Portanto poderíamos apenas calcular a integral entre -4 e 1.5. Melhor ainda seria tirar proveito do conhecimento que a probabilidade acumulada
   de uma distribuição normal até a média é 0.5 (50%) e então calcular a integral apenas de 0 a 1.5 e somar 0.5 (que é o valor pré-conhecido da integral até 0). Esse tipo de abordagem
   evita *muitos* cálculos desnecessários e pode reduzir consideravelmente o tempo de simulação de um modelo.
* Agora valor para o caso citado inicialmente: encontrar o valor x de uma distribuição de probabildiade cuja probabilidade acumulada corresponda a um valor dado.
* Por exemplo: Qual é o valor de x de uma curva normal padrão (média=0, desvio=1) tal que a probabilidade acumulada até x seja 0.4?
* Assumindo que podemos usar apenas o método "integrate" da clase "Solver" para calcular as integrais, teríamos que ficar "tentando" achar o valor "max" até que o valor da integral
   seja o valor dado. Nesse caso, max seria o valor x procurado, Isso e muito ineficiente.
* Uma abordagem mais interessante é utilizar o conhecimento disponível para definir limites iniciais aceitáveis, e então utilizar métodos numéricos análogos ao de "busca de raízes reais"
   para encontrar o valor x. No caso deste exemplo (Qual é o valor de x de uma curva normal padrão (média=0, desvio=1) tal que a probabilidade acumulada até x seja 0.4), poderíamos
   começar definindo o intervalo de busca entre -4 e 0, já que sabemos que a probabilidade acumulada nesses pois pontos é 0 e 0.5, respectivamente. Portanto o valor x cuja integral
   acumulada é 0.4 deve obrigatoriamente estar entre -4 e 0. Sendo g(x) a integral acumulada, então g(-4)=0 e g(0)=0.5. A pergunta é g(x)=0.4, qual é x?.
* O método da da secante para busca de raízes pode ser adaptado para resolver esse problema. Ao invés de procurar x tal que f(x)=0 (se é 0, é a raiz da função), procuramos x
   tal que g(x)=probabilidade acumulada desejada. Trata-se de um simples problema de equação de reta. Só isso. Se uma reta no ponto x=-4 passa por y=0 g(-4)=0
   e no ponto x=0 passa pelo ponto y=0.5 g(0)=05, então em qual ponto x ela pasa por y=0.4? Basta resolver a equação da reta e ter a próxima estimativa de onde procurar pela "raiz"
   dessa função. Se o valor encontrado for o procurado (ou muito próximo dele), terminamos. Senão, definimos o novo intervalo (que é menor que o anterior) e continuamos *recursivamente*
   a busca até encontrar a solução ou alcançar a quantidade máxima de recursões.
*/
class ProbabilityDistributionStudent : public ProbabilityDistributionBase {
public:

    /*!
    * Todos os métodos "inverseXYZ" abaixo devem retornar o valor de x tal que a probabilidade acumulada da distribuição XYZ até x seja "cumulativeProbability".
    * Esses métodos devem tirar proveito do conhecimento disponível sobre cada uma das distribuições de probabilidade para definir os intervalor iniciais para a "busca de raízes", ou
    *   melhor, a *busca pela probabilidade acumulada*.
    * Uma vez definidos esses intervalos, cada um desses métodos deve invocar uma função *recursiva* que implementa um método
    *   análogo ao da secante para busca de raízes (como explicado acima) e que refina essa busca em intervalos cada vez menores até encontrar o valor desejado ou alcançar a quantidade
    *   máxima de recursoes.
    * Esses métodos *recursivos* estão mais abaixo, e têm o nome "findInverseXYZ". Porém, os métodos "inverseXYZ" NÃO DEVEM invocá-los diretamente.
    * Para invocar um método "findInverseXYZ", deve-se usar "PDProxy::findInverseXYZ". A primeira chamada desse método recursivo deve usar o parâmetros "recursions"=0.
    * Outro aspecto muito importante nessa implementação, é que é comum durante uma simulação que o cada um desses métodos seja invocado milhares ou milhões de vezes com eatamente os mesmos
        parâmetros. Se os parâmetros de entrada são os mesmos de uma execução anterior, então o resultado já havia sido calculado antes. Para evitar o recálculo da mesma
        coisa milhões de vezes, é imprescindível que hava uma espécie de "cache", que mapeie o conjunto de parâmetros de entrada para o valor já calculado. Assim, antes de fazer qualquer
        cálculo, esses métodos deveriam primeiro verificar nessa "cache" se o que está sendo pedido já foi previamente calculado e, se foi, simplesmente retorne o valor da cache. Se não foi,
        então o cálculo descrito deve ser realziado e o resultado deve ser guardado na cache antes de ser retornado.
    */
	static double inverseChi2(double cumulativeProbability, double degreeFreedom){
	    double xLowerLimit, xUpperLimit;
        xLowerLimit = 0;
        xUpperLimit = 24*(1+ (degreeFreedom/10));

        //determinar a e b necessários
        double a = xLowerLimit;
        double b = xUpperLimit;

        std::cout << "lowerLimit = "<< xLowerLimit << ", upperLimit = " << xUpperLimit << ", probability = " << cumulativeProbability << std::endl;

        SolverProxy solver;
        double fa = 0;
        std::cout << "fa = "<< fa << std::endl;
        double fb = solver.integrate(xLowerLimit, b, &ProbabilityDistributionBase::chi2, degreeFreedom);
        std::cout << "fb = "<< fb << std::endl;
        double x = PDProxy::findInverseChi2(a, fa, b, fb, 0, cumulativeProbability, degreeFreedom);

        //probabilityValuesCache.push_back(std::tuple<double, double, double, double, double>(mean, stddev, xLowerLimit, x, cumulativeProbability));
        // retornar x tal que a integral de -infinito até x seja igual a cumulativeProbability
	    return x;
	}
	static double inverseFFisherSnedecor(double cumulativeProbability, double d1, double d2){
	    double xLowerLimit, xUpperLimit;
        xLowerLimit = 0;
        xUpperLimit = (1000/d1) + 5000/(5*pow(d2, 2));

        //determinar a e b necessários
        double a = xLowerLimit;
        double b = xUpperLimit;

        std::cout << "lowerLimit = "<< xLowerLimit << ", upperLimit = " << xUpperLimit << ", probability = " << cumulativeProbability << std::endl;

        SolverProxy solver;
        double fa = 0;
        std::cout << "fa = "<< fa << std::endl;
        double fb = solver.integrate(xLowerLimit, b, &ProbabilityDistributionBase::fisherSnedecor, d1, d2);
        std::cout << "fb = "<< fb << std::endl;
        double x = PDProxy::findInverseFFisherSnedecor(a, fa, b, fb, 0, cumulativeProbability, d1, d2);

        //probabilityValuesCache.push_back(std::tuple<double, double, double, double, double>(mean, stddev, xLowerLimit, x, cumulativeProbability));
        // retornar x tal que a integral de -infinito até x seja igual a cumulativeProbability
	    return x;
	}
	static double inverseNormal(double cumulativeProbability, double mean, double stddev){
        // distribuição acumulada em lowerLimit =~ 0
        double xLowerLimit = mean - 5*stddev;


        // distribuição acumulada em upperLimit =~ 1
        double xUpperLimit = mean + 5*stddev;

        // struct normalDistributionCacheEntry halfDistributionLower =
        //     {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = mean, .cumulativeProbability = 0.5};
        // insertInNormalCache(halfDistributionLower);
        // struct normalDistributionCacheEntry halfDistributionUpper =
        //     {.mean = mean, .stddev = stddev, .a = mean, .b = xUpperLimit, .cumulativeProbability = 0.5};
        // insertInNormalCache(halfDistributionUpper);

        // for (struct normalDistributionCacheEntry cachedValue : normalDistributionCache) {
        //     if (isClose(cachedValue.mean, mean) && isClose(cachedValue.stddev, stddev) &&
        //         isClose(cachedValue.cumulativeProbability, cumulativeProbability) && isClose(cachedValue.a, xLowerLimit)) {
        //             // std::cout << " Pegou valor já calculado na cache!" << std::endl;
        //             return cachedValue.b;
        //     }
        // }

        // determinar a e b necessários
        double a,b,fa,fb;

        SolverProxy solver;

        if (cumulativeProbability == 0.5) {
            return mean;
        } else if (cumulativeProbability > 0.5) {
            a = mean;
            fa = 0.5;
            b = xUpperLimit;
            fb = solver.integrate(xLowerLimit, b, &ProbabilityDistributionBase::normal, mean, stddev);
        } else {
            a = xLowerLimit;
            fa = 0;
            b = mean;
            fb = 0.5;
        }

        std::cout << "lowerLimit = "<< xLowerLimit << ", upperLimit = " << xUpperLimit << ", probability = " << cumulativeProbability << std::endl;

        double x = PDProxy::findInverseNormal(a, fa, b, fb, 0, cumulativeProbability, mean, stddev);

        struct normalDistributionCacheEntry result = {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = x, .cumulativeProbability = cumulativeProbability};
        insertInNormalCache(result);
        // retornar x tal que a integral de -infinito até x seja igual a cumulativeProbability
	    return x;
	}
	static double inverseTStudent(double cumulativeProbability, double mean, double stddev, double degreeFreedom){
        double xLowerLimit, xUpperLimit;
        xLowerLimit = - (318000/pow(degreeFreedom, 5) +900/pow(degreeFreedom, 2));
        xUpperLimit = (318000/pow(degreeFreedom, 5) +900/pow(degreeFreedom, 2));

        // determinar a e b necessários
        double a,b;
        if (cumulativeProbability == 0.5) {
            return 0;
        } else if (cumulativeProbability > 0.5) {
            a = 0;
            b = xUpperLimit;
        } else {
            a = xLowerLimit;
            b = 0;
        }

        std::cout << "lowerLimit = "<< a << ", upperLimit = " << b << ", probability = " << cumulativeProbability << std::endl;

        // usar integrais conhecidas de a e diminuir no cumulative probability

        double fa = ProbabilityDistributionBase::tStudent(a, mean, stddev, degreeFreedom);
        std::cout << "fa = "<< fa << std::endl;
        double fb = ProbabilityDistributionBase::tStudent(b, mean, stddev, degreeFreedom);
        std::cout << "fb = "<< fb << std::endl;
        double x = PDProxy::findInverseTStudent(a, fa, b, fb, 0, cumulativeProbability, mean, stddev, degreeFreedom);

        //probabilityValuesCache.push_back(std::tuple<double, double, double, double, double>(mean, stddev, xLowerLimit, x, cumulativeProbability));
        // retornar x tal que a integral de -infinito até x seja igual a cumulativeProbability
	    return x;
	}


    /*!
    * Os métodos "findInverseXYZ" abaixo são métodos *recursivos* recebem os limites inferior "a" e superior "b" do intervalo a pesquisar,  e também o valor da
       função (probabilidade acumulada) nesses dois pontos, que são f(a)="fa" e f(b)="fb", a quantidade de recursões "recursions" atuais, a probabilidade acumulada
       "cumulativeProbability" que se está procurando, e os demais parâmetros da distribuição de probabilidade de interesse.
    * Esses métodos devem, então, com base no método análogo ao da secante, e os valores conhecidos da probabilidade acumulada nos limites do intervalo ("fa" e "fb")
       calcular um ponto x denro desse intervalo (com base na equação de reta) que deve corresponder à probabilidade acumulada procurada.
    * Então deve calcular a probabilidade acumulada até esse valor, de maneira inteligente. Se o valor da probabilidade acumulada nesse ponto x for suficientemente
        próximo daquela procurada OU se a quantidade máxima de recursões já foi alcançada, retornar sua melhor estimativa. A quantidade máxima de iterações é "PDProxy::getMaxRecursions()".
    * Senão, com base no valor de f(x) (a probabilidade acumulada encontrada), definir um novo intervalo (que pdoe ser de a até x ou de x até b), incrementar a quantidade
        de recursões e invocar recursivamente esse método para continuar a procura.
    * Atenção: Para invocar recursivamente o método "findInverseXYZ" você DEVE invocar "PDProxy::findInverseXYZ".
    * Como o cálculo das integrais será invocado muitas vezes recursivamente, e a própria invocação de cada método "inverseXYZ" pode ocorrer milhares ou milhões de vezes
        em cada simulação, é imprescindível fazer uma invocação inteligente das integrais, evitando qualquer recálculo desnecessário.
    * Exemplo: Suponha que esse método seja invocado com a=10, fa=0.3 e b=20. Suponha ainda que =, conforme a equação da reta, o valor estimado para x seja 15.
    * Isso significa que devemos calcular a integral acumulada até x=15. Calcular a integral de -infinito até 15 não é aceitável, uma vez que já se sabe que a integral
         acumulada até a=10 é fa=0.3. Portanto, o que deveria ser feito é calcular a integral de 10 até 15 e somar 0.3 a ela.

    * Nos métodos abaixo, então, você vai precisar calcular a integral de uma distribuição de probabilidade. Não use diretamente a sua classe "SolverStudent" para invocar
        os métodos "integrate". Ao contráio, você DEVE usar os métodos de mesmo nome, mas da classe "SolverProxy".
    * Para invocar o "integrate" você deve passar um parâmetro com o ponteiro para a função a ser integrada, que seve ser a distribuição de probabilidade de interesse.
    * Para fazer isso, você pode passar o ponteiro para um dos seguintes métodos estáticos da class abaixo.
        class ProbabilityDistributionBase {
    	    static double chi2(double x, double degreeFreedom);
	        static double fisherSnedecor(double x, double d1, double d2);
	        static double normal(double x, double mean, double stddev);
	        static double tStudent(double x, double mean, double stddev, double degreeFreedom);
    */

	static double findInverseChi2(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double degreeFreedom){

        if (PDProxy::getMaxRecursions() == recursions) {
            return b;
        }

        SolverProxy solver;

        double currentProbability = cumulativeProbability - fa;
        double approximateDerivative = (currentProbability / (fb - fa))*(b-a);
        double root = a + approximateDerivative;
        double fr = solver.integrate(a, b, &ProbabilityDistributionBase::chi2, degreeFreedom) + fa;

        std::cout << "Iteração " << recursions + 1 <<": froot = "<< fr << " probabilidade esperada =  " << cumulativeProbability << " root =  " << root << std::endl;

        double maxValue = fmax(fr, cumulativeProbability);
        if (abs(fr - cumulativeProbability)/maxValue < 1e-3) {
            return root;
        }

        if (fr < cumulativeProbability) {
            return PDProxy::findInverseChi2(root, fr, b, fb, ++recursions, cumulativeProbability, degreeFreedom);  
        } else {
            return PDProxy::findInverseChi2(a, fa, root, fr, ++recursions, cumulativeProbability, degreeFreedom);  
        }
	}
	static double findInverseFFisherSnedecor(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double d1, double d2){
	    if (PDProxy::getMaxRecursions() == recursions) {
            return b;
        }

        SolverProxy solver;

        double currentProbability = cumulativeProbability - fa;
        double approximateDerivative = (currentProbability / (fb - fa))*(b-a);
        double root = a + approximateDerivative;
        double fr = solver.integrate(a, b, &ProbabilityDistributionBase::fisherSnedecor, d1, d2) + fa;

        std::cout << "Iteração " << recursions + 1 <<": froot = "<< fr << " probabilidade esperada =  " << cumulativeProbability << " root =  " << root << std::endl;

        double error = abs(fr - cumulativeProbability);
        std::cout << "Erro =  " << error << std::endl;
        if (abs(fr - cumulativeProbability) < 1e-2) {
            return root;
        }

        if (fr < cumulativeProbability) {
            return PDProxy::findInverseFFisherSnedecor(root, fr, b, fb, ++recursions, cumulativeProbability, d1, d2);  
        } else {
            return PDProxy::findInverseFFisherSnedecor(a, fa, root, fr, ++recursions, cumulativeProbability, d1, d2);  
        }
	}
	static double findInverseNormal(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev){
        if (PDProxy::getMaxRecursions() == recursions) {
            return b;
        }
        // double xLowerLimit = mean - 5*stddev;

        // double integralA = -1, integralB = -1, integralValue = -1;

        // for (struct normalDistributionCacheEntry cachedValue : normalDistributionCache) {
        //     if (isClose(cachedValue.mean, mean) && isClose(cachedValue.stddev, stddev)) {
        //         if (isClose(cachedValue.b, a) && isClose(cachedValue.a, xLowerLimit)) {
        //             integralA = cachedValue.cumulativeProbability;
        //         }
        //         if (isClose(cachedValue.b, b) && isClose(cachedValue.a, xLowerLimit)) {
        //             integralB = cachedValue.cumulativeProbability;
        //         }
        //         if (isClose(cachedValue.a, a) && isClose(cachedValue.b, b)) {
        //             integralValue = cachedValue.cumulativeProbability;
        //         }
        //     }
        // }

        // SolverProxy solver;

        // if (integralA == -1) {
        //     integralA = solver.integrate(xLowerLimit, a, &ProbabilityDistributionBase::normal, mean, stddev);
        //     struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = a, .cumulativeProbability = integralA};
        //     insertInNormalCache(newEntry);
        // }
        // if (integralB == -1) {
        //     integralB = solver.integrate(xLowerLimit, b, &ProbabilityDistributionBase::normal, mean, stddev);
        //     struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = b, .cumulativeProbability = integralB};
        //     // std::cout << "{ mean = "<< newEntry.mean << ", stddev = " << newEntry.stddev << ", a = " << newEntry.a << ", b = "<< newEntry.b << ", cumulativeProbability = " << newEntry.cumulativeProbability << "}" << std::endl;
        //     insertInNormalCache(newEntry);
        // }

        // if (a > b && integralB < cumulativeProbability) {
        //     if (integralValue == -1) {
        //         integralValue = solver.integrate(b, a, &ProbabilityDistributionBase::normal, mean, stddev);
        //         struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = b, .b = a, .cumulativeProbability = integralValue};
        //     }
        //     integralValue += integralB;
        //     struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = a, .cumulativeProbability = integralValue};
        // } else if (integralA < cumulativeProbability) {
        //     if (integralValue == -1) {
        //         integralValue = solver.integrate(a, b, &ProbabilityDistributionBase::normal, mean, stddev);
        //         struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = a, .b = b, .cumulativeProbability = integralValue};
        //         insertInNormalCache(newEntry);
        //     }
        //     integralValue += integralA;
        // } else if (integralValue == -1) {
        //     integralValue = solver.integrate(a, b, &ProbabilityDistributionBase::normal, mean, stddev);
        // }

        // struct normalDistributionCacheEntry newEntry = {.mean = mean, .stddev = stddev, .a = xLowerLimit, .b = b, .cumulativeProbability = integralValue};
        // insertInNormalCache(newEntry);

        // // std::cout << "Iteração " << recursions + 1 <<": integral = "<< integralValue << std::endl;
        // // std::cout << "probabilidade esperada =  " << cumulativeProbability << std::endl;

        // double maxValue = fmax(integralValue, cumulativeProbability);
        // if (abs(integralValue - cumulativeProbability)/maxValue < 1e-3) {
        //     // std::cout << "integral - probability = " << integralValue - cumulativeProbability << std::endl;
        //     // std::cout << "Retorno = " << b << std::endl;degreeFreedom

        // a = b;
        // fa = fb;
        // b = root;
        // fb = ProbabilityDistributionBase::normal(b, mean, stddev);

        // return PDProxy::findInverseNormal(a, fa, b, fb, ++recursions, cumulativeProbability, mean, stddev);

        SolverProxy solver;

        double currentProbability = cumulativeProbability - fa;
        double approximateDerivative = (currentProbability / (fb - fa))*(b-a);
        double root = a + approximateDerivative;

        // double approximateDerivative = (fb - fa)*b/((b-a));
        // std::cout << "Derivada aproximada = " << approximateDerivative << std::endl;
        // double root = a - (fa/approximateDerivative);

        double fr = solver.integrate(a, b, &ProbabilityDistributionBase::normal, mean, stddev) + fa;

        std::cout << "Iteração " << recursions + 1 <<": froot = "<< fr << " probabilidade esperada =  " << cumulativeProbability << " root =  " << root << std::endl;

        double maxValue = fmax(fr, cumulativeProbability);
        if (abs(fr - cumulativeProbability)/maxValue < 1e-4) {
            return root;
        }

        if (fr < cumulativeProbability) {
            return PDProxy::findInverseNormal(root, fr, b, fb, ++recursions, cumulativeProbability, mean ,stddev);  
        } else {
            return PDProxy::findInverseNormal(a, fa, root, fr, ++recursions, cumulativeProbability, mean, stddev);  
        }
	}
	static double findInverseTStudent(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev, double degreeFreedom){
	    if (PDProxy::getMaxRecursions() == recursions) {
            return b;
        }
        double xLowerLimit = - (318000/pow(degreeFreedom, 5) +900/pow(degreeFreedom, 2));

        SolverProxy solver;

        double integralA = solver.integrate(xLowerLimit, a, &ProbabilityDistributionBase::tStudent, mean, stddev, degreeFreedom);
        double integralB = solver.integrate(xLowerLimit, b, &ProbabilityDistributionBase::tStudent, mean, stddev, degreeFreedom);

        double integralValue;
        if (a > b && integralB < cumulativeProbability) {
            integralValue = solver.integrate(b, a, &ProbabilityDistributionBase::tStudent, mean, stddev, degreeFreedom) + integralB;
        } else if (integralA < cumulativeProbability) {
            integralValue = solver.integrate(a, b, &ProbabilityDistributionBase::tStudent, mean, stddev, degreeFreedom) + integralA;
        } else {
            integralValue = solver.integrate(a, b, &ProbabilityDistributionBase::tStudent, mean, stddev, degreeFreedom);
        }

        std::cout << "Iteração " << recursions + 1 <<": integral = "<< integralValue << std::endl;
        std::cout << "probabilidade esperada =  " << cumulativeProbability << std::endl;

        double maxValue = fmax(integralValue, cumulativeProbability);
        if (abs(integralValue - cumulativeProbability)/maxValue < 1e-3) {
            std::cout << "integral - probability = " << integralValue - cumulativeProbability << std::endl;
            std::cout << "Retorno = " << b << std::endl;
            return fmax(a,b);
        }

        // implementar método da secante p/ integral e achar valores de a e b novos
        std::cout << "Integral de a (-infinito até " << a <<") = " << integralA << std::endl;
        std::cout << "Integral de b (-infinito até " << b <<") = " << integralB << std::endl;
        double approximateDerivative = (integralB - integralA)*degreeFreedom/((b-a));
        std::cout << "Derivada aproximada = " << approximateDerivative << std::endl;
        double root = a - (integralA/approximateDerivative);
        std::cout << "Root = " << root << std::endl;

        
        a = b;
        fa = fb;
        b = root;
        fb = fb = ProbabilityDistributionBase::tStudent(b, mean, stddev, degreeFreedom);

        return PDProxy::findInverseTStudent(a, fa, b, fb, ++recursions, cumulativeProbability, mean, stddev, degreeFreedom);  
	}
};

#endif /* PROBABILITYDISTRIBUTIONSTUDENT_H */