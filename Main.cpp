#include <stdlib.h>
#include <iostream>
#include <cmath>
#include <string>
#include <random>
#include <vector>

#include "test.h"
#include "SolverProxy.h"
#include "ProbabilityDistributionBase.h"
#include "PDProxy.h"
#include "DAProxy.h"
#include "Legendre.h"

using namespace std;

double seno(double x) {
	return sin(x);
}

double senoPlusCosseno1(double x) {
	return sin(x)+cos(x)+1;
}

void fex1(int *n, double *t, double *y, double *ydot);

// cout << "Scilab deff(' [W]=f(x,y)',['fi=y(2)+x';'f2=y(1)+y(2)';'w=[f1:f2]'))" << end1;
double difEq1_0(double t, double y1, double y2) {
	return y2+t;
}
double difEq1_1(double t, double y1, double y2) {
return -y1+y2;
}

//
// SIR infection disease model
// y1 = Susceptible; y2 = Infected ; y3 = Recovered
double betha = 0.4; // rate of infection
double alpha = 0.2; // rate of recover
double difEq2_0(double t, double y1, double y2, double y3) {
	return -betha*y1*y2;
}
double difEq2_1(double t, double y1, double y2, double y3) {
	return betha*y1*y2 - alpha*y2;
}
double difEq2_2(double t, double y1, double y2, double y3) {
	return alpha*y2;
}
//
// ATP e G biochemical model
// cout << "Scilab deff('[w]=f(x,y)',['f1=2*k1*y(2)*y(1) - kp*y(1)/(y(1)+km)';'f2=vin-k1*y(2)*y(1)';'w=[f1;f2]'])" << endl:
double k1=0.02;
double kp=6;
double km=13;
double vin=0.36;
double difEq3_0(double t, double y1, double y2) {
return 2*k1*y2*y1 - kp*y1/(y1+km);
}
double difEq3_1(double t, double y1, double y2) {
	return vin - k1*y2*y1;
}

// dx/dt = x+2y+1
// dy/dt = -x+y+t
double difEq4_0(double t, double y1, double y2) {
	return y1+2*y2+1;
}
double difEq4_1(double t, double y1, double y2) {
	return -y1+y2+t;
}

int test(int num) {
	int errors = 0;
	double value, value2;
	switch (num) {

		/*
			INTEGRAÇÃO — funcionalidade
		*/

		case 1: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver->integrate(0.0, 3.14159265358979323846, &seno)" << endl;
			cout << "Scilab y=integrate('sin(x)','x',0,%pi)" << endl;
			solver->setMaxSteps(1e3);
			value = solver->integrate(0.0, 3.14159265358979323846, &seno);
			errors += TEST_EQUAL_FP(value, 2.0);
			break;
		}
		case 2: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver—>integrate(-1.0, 0.0, &ProbabilityDistributionBase::normal, 0.0, 1.0)" << endl;
			cout << "Scilab cdfnor(\"PQ\", 0, 0, 1) - cdfnor(\"PQ\", -1, 0, 1)" << endl;
			solver->setMaxSteps(1e3);
			value = solver->integrate(-1.0, 0.0, &ProbabilityDistributionBase::normal, 0.0, 1.0);
			errors += TEST_EQUAL_FP(value, 0.341344746068542925777);
			break;
		}
		case 3: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver->integrate(-400, 0.0, &ProbabilityDistributionBase::normal, 1000.0, 200.0)" << endl;
			cout << "Scilab cdfnor(\"PQ\",0, 1000, 200)-cdfnor(\"PQ\", -400, 1000, 200)" << endl;
			solver->setMaxSteps(1e3);
			value = solver->integrate(-400, 0.0, &ProbabilityDistributionBase::normal, 1000.0, 200.0);
			errors += TEST_EQUAL_FP(value, 0.000000286650292066650);
			break;
		}
		case 4: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver->integrate(1e3, 3e3, &senoPlusCosseno1)" << endl;
			cout << "Scilab y=integrate('sin(x)+cos(x)41','x',1e3,3e3)" << endl;
			solver->setMaxSteps(1e3);
			value = solver->integrate(1e3, 3e3, &senoPlusCosseno1);
			errors += TEST_EQUAL_FP(value, 2000.930371709927612756);
			break;
		}


		/*
			DERIVAÇÃO - funcionalidade
		*/

		case 5: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver->derivate(0.0, 2.0, {1.0, 2.0}, {difEq1_0, difEq1_1})" << endl;
			cout << "Scilab deff('[w]=f(x,y)',['f1=y(2)+x'; 'f2=-y(1)+y(2)'; ‘w=[f1;f2)'])" << endl;
			cout << "x0=0; xn=2; Dx=(xn-x0)/1e3; y0=[1;2]; x=[x0:Dx:xn];" << endl;
			cout << "y = ode(y0,x0,x,f)" << endl;
			solver->setMaxSteps(1e3);
			std::vector<double> initVal = {1.0, 2.0};
			std::vector<Solver_if::f3p> f = {difEq1_0, difEq1_1};
			std::vector<double> result = solver->derivate(0.0, 2.0, initVal, f);
			errors += TEST_EQUAL_FP(result[0], 5.308764885027023261443);
			errors += TEST_EQUAL_FP(result[1], -2.760273444378841034563);
			break;
		}
		case 6: {
			// SIR infection disease model
			SolverProxy* solver = new SolverProxy();
			cout << "solver->derivate(0.0, 365.0, {100.0, 0.0, 0.0}, {betha*y1*y2; betha*y1*y2-alpha*y2; alpha*y2})" << endl;
			cout << "SIR infection disease model; betha=0.4; alpha=0.2; [f1=betha*y1*y2; f2=betha*y1*y2 - alpha*y2; f3=alpha*y2;]" << endl;
			solver->setMaxSteps(1e3);
			std::vector<double> initVal = {100, 0.0, 0.0}; // all people are susceptible
			std::vector<Solver_if::f4p> f = {difEq2_0, difEq2_1, difEq2_2};
			std::vector<double> result = solver->derivate(0.0, 365.0, initVal, f);
			errors += TEST_EQUAL_FP(result[0], 20.0);
			errors += TEST_EQUAL_FP(result[1], 0.0);
			errors += TEST_EQUAL_FP(result[2], 80.0);
			break;
		}
		case 7: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver—>derivate(0.0, 200.0, {1.0, 2.0}, {2*ki*y2*y1-kp*y1/(y1+km); vin-ki*y2*y1})" << endl;
			cout << "ATP/G biochemical oscilatory model; Scilab deff('[w]=f(x,y)',['f1=2*k1*y(2)*y(1) - kp*y(1)/(y(1)+km)';'f2=vin-k1*y(2)*y(1)';'w=[f1;f2]'])" << endl;
			cout << "k1=0.02; kp=6; km=13; vin=0.36" << endl;
			cout << "x0=0; xn=200; Dx=(xn-x0)/1e3; y0=[1;2]; x=[x0:Dx:xn];" << endl;
			cout << "y = ode(y0, x0 ,x, f)" << endl;
			solver->setMaxSteps(1e3);
			std::vector<double> initVal = {1.0, 2.0};
			std::vector<Solver_if::f3p> f = {difEq3_0, difEq3_1};
			std::vector<double> result = solver->derivate(0.0, 200.0, initVal, f);
			errors += TEST_EQUAL_FP(result[0], 5.38726805118368812231);
			errors += TEST_EQUAL_FP(result[1], 15.02886918544643179985);
			break;
		}
		case 8: {
			SolverProxy* solver = new SolverProxy();
			cout << "solver->derivate(-1.0, 7.0, {2.0, -1.0}, {y1+2*y2+1; -y1+y2+t})" << endl;
			cout << "Scilab deff(' [wl=f(x,y)', ['f1=y(1)+2*y(2)+1'; f2=-y(1)+y(2)+x';'w=[f1;f2]'])" << endl;
			cout << "x0=-1; xn=7; Dx=(xn-x0)/1e3: y0=[2;-1]; x=[x0:Dx:xn);" << endl;
			cout << "y = ode(y0,x0,x,f)" << endl;
			solver->setMaxSteps(1e3);
			std::vector<double> initVal = {2.0, -1.0};
			std::vector<Solver_if::f3p> f = {difEq4_0, difEq4_1};
			std::vector<double> result = solver->derivate(-1.0, 7.0, initVal, f);
			errors += TEST_EQUAL_FP(result[0], 6836.733340746551220946);
			errors += TEST_EQUAL_FP(result[1], 4077.8568461106583527);
			break;
		}

		/*
			DISTRIBUIÇÃO INVERSA — funcionalidade
		*/

		case 9: {
			cout << "PDProxy::inverseNormal(0.925, 100.0, 30.0)" << endl;
			cout << "=NORM.INV(0,925;100;30)" << endl;
			value = PDProxy::inverseNormal(0.925, 100.0, 30.0);
			errors += TEST_EQUAL_FP(value, 143.185944128154);
			break;
		}
		case 10: {
			cout << "PDProxy::inverseChi2(0.85, 20)" << endl;
			cout << "=CHIINV(O,85; 20)" << endl;
			value = PDProxy::inverseChi2(0.85, 20);
			errors += TEST_EQUAL_FP(value, 13.6038595449049);
			break;
		}
		case 11: {
			cout << "PDProxy::inverseFFisherSnedecor(0.875, 22, 13)" << endl;
			cout << "=F.INV(0,875; 22; 13)" << endl;
			value = PDProxy::inverseFFisherSnedecor(0.875, 22, 13);
			errors += TEST_EQUAL_FP(value, 1.85693112958976);
			break;
			}
		case 12: {
			cout << "PDProxy::inverseTStudent(0.975, 0.0, 1.0, 15)" << endl;
			cout << "=T.INV(0,975; 15)" << endl;
			value = PDProxy::inverseTStudent(0.975, 0.0, 1.0, 15);
			errors += TEST_EQUAL_FP(value, 2.13144954555978);
			break;
		}

		/*
			DISTRIBUIÇÃO INVERSA — eficiência
		*/

		case 13: {
			cout << "PDProxy::inverseNormal(0.975, -400.0, 20.0)" << endl;
			// =NORM. INV(0,975;0;1)3*20 -400
			value = PDProxy::inverseNormal(0.975, -400.0, 20.0);
			errors += TEST_EQUAL_FP(value, -360.800720309199);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 50, "Limite máximo de invocações");
			value = PDProxy::inverseNormal (0.975, -401.0, 21.0); // any other
			PDProxy::setCount(0);
			cout << "PDProxy::inverseNormal (0.975, -400.0, 20.0)" << endl;
			value = PDProxy::inverseNormal (0.975, -400.0, 20.0);
			errors += TEST_EQUAL_FP(value, -360.800720309199);
			value = PDProxy:: getCount();
			errors += TEST_LESS<double>(value, 1, "Limite máximo de invocações");
			break;
		}
		case 14: {
			cout << "PDProxy::inverseChi2(0.5, 30)" << endl;
			// =CHIINV(0,5; 30)
			value = PDProxy::inverseChi2(0.5, 30);
			errors += TEST_EQUAL_FP(value, 29.3360315166616);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 10, "Limite máximo de invocações");
			value = PDProxy::inverseChi2(0.55, 31); // any other
			PDProxy::setCount(0);
			cout << "PDProxy::inversechi2(0.5, 30)" << endl;
			value = PDProxy::inverseChi2(0.5, 30);
			errors += TEST_EQUAL_FP(value, 29.3360315166616);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 1, "Limite máximo de invocações");
			break;
		}

		case 15: {
			cout << "PDProxy::inverseFFisherSnedecor(0.99, 35, 17)" << endl;
			// =F.INV(0,99; 35; 17)
			value = PDProxy::inverseFFisherSnedecor(0.99, 35, 17);
			errors += TEST_EQUAL_FP(value, 2.95626585030618);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 10, "Limite máximo de invocações");
			value = PDProxy::inverseFFisherSnedecor(0.99, 30, 20); // any other
			PDProxy::setCount(0);
			cout << "PDProxy::inverseFFisherSnedecor(0.99, 35, 17)" << endl;
			value = PDProxy::inverseFFisherSnedecor(0.99, 35, 17);
			errors += TEST_EQUAL_FP(value, 2.95626585030618);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 1, "Limite máximo de invocações");
			break;
		}
		case 16: {
			cout << "PDProxy::inverseTStudent(0.025, 0.0, 1.0, 10)" << endl;
			// =T.INV(0,025; 10)
			value = PDProxy:: inverseTStudent(0.025, 0.0, 1.0, 10);
			errors += TEST_EQUAL_FP(value, -2.22813885198627);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 10, "Limite máximo de invocações");
			value = PDProxy::inverseTStudent (0.025, 0.0, 1.0, 8); // any other
			PDProxy::setCount(0);
			cout << "PDProxy::inverseTStudent(0.025, 0.0, 1.0, 10)" << endl;
			value = PDProxy::inverseTStudent(0.025, 0.0, 1.0, 10);
			errors += TEST_EQUAL_FP(value, -2.22813885198627);
			value = PDProxy::getCount();
			errors += TEST_LESS<double>(value, 1, "Limite máximo de invocações");
			break;
		}

		/*
			MÉDIAS MÓVEIS
		*/

		case 17: {
			cout << "DataAnalyserStudent->movingAverage(10, 2)" << endl;
			std::random_device dev;
			std::mt19937 rng(dev());
			std::uniform_int_distribution<std::mt19937::result_type> unif(0, 1e2);
			const unsigned int n=10;
			cout << "Original values: ";
			for (unsigned int i=0; i<n; i++) {
				value = unif(rng)/1.0;
				cout << value << ", ";
				DAProxy::setDatum(i, value);
			}
			cout << endl;
			DAProxy* da = new DAProxy();
			vector<double> res = da->movingAverage(n, 2);
			errors += TEST_EQUAL_FP(DAProxy::getDatum(0), res[0], "Primeiro valor");
			errors += TEST_EQUAL_FP(DAProxy:: getDatum(n-1), res[n-1], "Último valor");
			value = (DAProxy:: getDatum(0)+DAProxy::getDatum(1)+DAProxy::getDatum(2))/3.0;
			value2 = (res[0]+res[1]+res[2])/3.0;
			errors += TEST_EQUAL_FP(value, value2, "Segundo valor");
			value = (DAProxy::getDatum(n-1)+DAProxy::getDatum(n-2)+DAProxy::getDatum(n-3))/3.0;
			value2 = (res[n-1]+res[n-2]+res[n-3])/3.0;
			errors += TEST_EQUAL_FP(value, value2, "Terceiro valor");
			//cout << "Saída" << endl;
			//for (unsigned int i=0; i<n; i++) {
				///cout << res[i] << endl;
			//}
			//errors += TEST_EQUAL<string>("\"Test\"", "\"Not implemented yet\"");
			break;
			}
			case 18: {
				cout << "DataAnalyserStudent->movingAverage(100, 10)" << endl;
				std::random_device dev;
				std::mt19937 rng(dev());
				std::uniform_int_distribution<std::mt19937::result_type> unif(0, 1e2);
				const unsigned int n=100;
				const unsigned int k=10;
				cout << "Original values: ";
				for (unsigned int i=0; i<n; i++) {
					value = unif(rng)/1.0;
					cout << value << ", ";
					DAProxy::setDatum(i, value);
				}
				cout << endl;
				DAProxy* da = new DAProxy();
				vector<double> res = da->movingAverage(n, k);
				unsigned int v=n/2;
				value = 0.0;
				value2 = 0.0;
				for (unsigned int i=v-k; i<=v+k; i++) {
					value += DAProxy::getDatum(i);
					value2 += res[i];
				}
				errors += TEST_EQUAL_FP(value/k, value2/k, "Valor no meio dos dados");
				v=n-k;
				value = 0.0;
				value2 = 0.0;
				for (unsigned int i=v-k-1; i<=v+k-1; i++) {
					value += DAProxy:: getDatum(i);
					value2 += res[i];
				}
				errors += TEST_EQUAL_FP(value/(k-1), value2/(k-1), "Valor quase no final dos dados");
				break;
			}
			case 19: {
				cout << "DataAnalyserStudent->movingaverage(30, 10)" << endl;
				std::random_device dev;
				std::mt19937 rng(dev());
				std::uniform_int_distribution<std::mt19937::result_type> unif(0, 162);
				const unsigned int n=30;
				const unsigned int k=10;
				cout << "Original values: ";
				for (unsigned int i=0; i<n; i++) {
					value = unif(rng)/1.0;
					cout << value << ", ";
					DAProxy::setDatum(i, value);
				}
				cout << endl;
				DAProxy* da = new DAProxy();
				vector<double> res = da->movingAverage(n, k);
				for (unsigned int i=0; i<n; i++) {
					value = DAProxy::getCount(i);
					errors += TEST_EQUAL<unsigned int>(value, 1, "Quantidade de acessos ao item " + to_string(i));
				}
				break;
			}
			case 20: {
				errors += TEST_EQUAL<string>("\"Test\"", "\"Not implemented yet\"");
				break;
			}


			default:
				errors += TEST_EQUAL("\"Test Number\"", "\"1-19\"");
		}
		return errors;
}

int main (int argc, char** argv) {
	cout << "Type test number: ";
	int testNum, res;
	std::cin >> testNum;
	cout << "Starting Test " << testNum << endl;
	res = test(testNum);
	string stdres = res==0?"Success":"Fail ("+ to_string(res) + ")";
	cout << "End Test " << testNum << ": " << stdres << endl;
	return res;
}
