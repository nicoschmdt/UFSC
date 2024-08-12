#ifndef SOLVER_IF_H
#define SOLVER_IF_H

#include <vector>
/*!
 * Interface used by classes that perform the numerical integration and derivation of functions with from one up to four parameters.
 * It is mainly used for calculating the probability of theoretical distributions, from its probability distribution functions.
 * p1 is the value where function is being evaluated and p2, ... are the function parameters
 */

class Solver_if {
public:
    typedef double (*f1p) (double);
    typedef double (*f2p)(double, double);
    typedef double (*f3p)(double, double, double);
    typedef double (*f4p)(double, double, double, double);
    typedef double (*f5p)(double, double, double, double, double);
public:
    virtual void setMinimumStepSize(double e) = 0;
    virtual double getMinimumStepSize() = 0;
    virtual void setMaxSteps(double steps) = 0;
    virtual double getMaxSteps() = 0;
    virtual double integrate(double min, double max, f1p) = 0;
    virtual double integrate(double min, double max, f2p, double p2) = 0;
    virtual double integrate(double min, double max, f3p, double p2, double p3) = 0;
    virtual double integrate(double min, double max, f4p, double p2, double p3, double p4) = 0;
    virtual double integrate(double min, double max, f5p, double p2, double p3, double p4, double p5) = 0;
public:
    virtual std::vector<double> derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f2p> f) = 0;
    virtual std::vector<double> derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f3p> f) = 0;
    virtual std::vector<double> derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f4p> f) = 0;
    virtual std::vector<double> derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f5p> f) = 0;
};

#endif /* SOLVER_IF_H */
