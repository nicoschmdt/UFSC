#ifndef SOLVERPROXY_H
#define SOLVERPROXY_H

#include "Solver_if.h"
class SolverProxy {
    public:
        SolverProxy();
        Solver_if* proxy;
        void setMinimumStepSize(double e);
        double getMinimumStepSize();
        void setMaxSteps(double steps);
        double getMaxSteps();
        double integrate(double min, double max, Solver_if::f1p f);
        double integrate(double min, double max, Solver_if::f2p f, double p2);
        double integrate(double min, double max, Solver_if::f3p f, double p2, double p3);
        double integrate(double min, double max, Solver_if::f4p f, double p2, double p3, double p4);
        double integrate(double min, double max, Solver_if::f5p f, double p2, double p3, double p4, double p5);
        std::vector<double>  derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f2p> f);
        std::vector<double>  derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f3p> f);
        std::vector<double>  derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f4p> f);
        std::vector<double>  derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f5p> f);

    private:
};

#endif /* SOLVERPROXY_H */