#ifndef DATAANALYSER_STUDENT_H
#define DATAANALYSER_STUDENT_H

#include <iostream>
#include <string>
#include <vector>
#include <deque>

#include "DAProxy.h"

/*!
* Essa classe, por enquanto, possui um único método para o cálculo do método numérico das médias móveis de "k" períodos sobre um conjunto de dados
    de "n" valores. 
*/
class DataAnalyserStudent {
public:
    DataAnalyserStudent() {
    }
    
    
    /*!
    * Este método deve retornar um vetor de "n" doubles que corresponda a um conjunto de dados suavizados pelo método numérico de médias móveis
        de "k" períodos sobre um conjunto inicial de dados com "n" valores.
    * Cada ponto "i" do conjunto de dados inicial deve ser substituido por uma média desse i-ésimo ponto com "k" pontos antes dele e "k" pontos depois 
        dele (ou seja, uma média de 2k+1 pontos). As exceções a essa regra são os pontos no começo e no final do conjunto de dados, do seguinte modo:
    * O primeiro e o último pontos (pontos 0 e n-1) são iguais (uma média deles e 0 pontos antes e depois). O segundo e o penúltim o pontos (1 e n-2) devem
        ser a média deles e 1 ponto antes e 1 ponto depois, e assim do ponto 0 até o ponto k-1 e do ponto n-1 retrocedendo até o ponto n-k.
    * Para ter acesso ao valor "i" do conjunto de dados original, deve-se invocar o método "DAProxy::getDatum(unsigned int i)", que retorna um double, que é
        o i-ésimo valor desse conjunto (de 0 a n-1).
    * Esse método deve ser eficiente, no sentido não precisar recalcular somas já feitas para os cálculos das médias. Com isso, também não deveria ler cada dado
        original mais de uma vez, e nem guardar mais do que 2k+1 valores. Um buffer circular de tamanho máximo 2k+1 para o cálculo das médias pode ser uma boa solução.
    */
    std::vector<double> movingAverage(unsigned int n, unsigned short k) {
       auto max_circular = 2*k + 1;
       auto lista_circular = std::deque<double>{};
       auto dados_suavizados = std::vector<double>{};
       auto get2 = k;
       auto quanto_adicionar_no_index = 1;
       
       for (int i=0; i<n; i++) {
        //   auto quanto_pegar = 2*k+1;
        //   auto quanto_adicionar = 1;
        //   if(get2 > 0 and !lista_circular.empty()) {
        //       get2 -= 1;
        //       quanto_adicionar = 2;
        //   } else if (i+k >= n) {
        //       quanto_adicionar = 0;
        //   }
           
        //   auto index = i;
        //   if (!lista_circular.empty()) {
        //       if (quanto_adicionar != 2) {
        //           index += k;
        //       } else if (i==1 || i==2) {
        //           if (i==2) {
        //               index += 1;   
        //           }
        //       } else {
        //           quanto_adicionar_no_index += 1;
        //           index += quanto_adicionar_no_index;
        //       }
        //   }
           
        //   //calcula o k pra frente
        //   for (int j=0; j<quanto_adicionar; j++) {
        //       double data = DAProxy::getDatum(index);
        //       if(!(lista_circular.size() < max_circular)) {
        //           lista_circular.pop_front();
        //       }
        //       lista_circular.push_back(data);
        //       index += 1;
        //   }
           
        //   auto somatotal = 0.0;
        //   if (i+k >= n) {
        //       quanto_pegar = (n-i-1)*2 + 1;
        //       auto index_final = lista_circular.size()-1;
        //       for (int j=quanto_pegar; j>0; j--) {
        //           somatotal += lista_circular.at(index_final);
        //           index_final--;
        //       }
        //   } else {
        //       for (auto&& value: lista_circular) {
        //           somatotal += value;
        //       }
        //       quanto_pegar = lista_circular.size();
        //   }
           
        //   auto dadoFinalDeI = somatotal/quanto_pegar;
        //   dados_suavizados.push_back(dadoFinalDeI);
            double data = DAProxy::getDatum(i);
            dados_suavizados.push_back(data);
       }
       return dados_suavizados;
    }
private:
};

#endif /* DATAANALYSER_STUDENT_H */

