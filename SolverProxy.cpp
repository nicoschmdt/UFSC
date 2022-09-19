#include "SolverProxy.h"
#include "SolverStudent.h"

SolverProxy::SolverProxy() {
    proxy = (Solver_if*) new SolverStudent();
}

void SolverProxy::setMinimumStepSize(double e) {
    proxy->setMinimumStepSize(e);
}
double SolverProxy::getMinimumStepSize() {
    return proxy->getMinimumStepSize();
}
void SolverProxy::setMaxSteps(double steps) {
    proxy->setMaxSteps(steps);
}
double SolverProxy::getMaxSteps() {
    return proxy->getMaxSteps();
}
double SolverProxy::integrate(double min, double max, Solver_if::f1p f) {
    return proxy->integrate(min, max, f);
}
double SolverProxy::integrate(double min, double max, Solver_if::f2p f, double p2) {
    return proxy->integrate(min, max, f, p2);
}
double SolverProxy::integrate(double min, double max, Solver_if::f3p f, double p2, double p3) {
    return proxy->integrate(min, max, f, p2, p3);
}
double SolverProxy::integrate(double min, double max, Solver_if::f4p f, double p2, double p3, double p4) {
    return proxy->integrate(min, max, f, p2, p3, p4);
}
double SolverProxy::integrate(double min, double max, Solver_if::f5p f, double p2, double p3, double p4, double p5) {
    return proxy->integrate(min, max, f, p2, p3, p4, p5);
}

std::vector<double> SolverProxy::derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f2p> f) {
    return proxy->derivate(initPoint, endPoint, initValue, f);
}
std::vector<double> SolverProxy::derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f3p> f) {
    return proxy->derivate(initPoint, endPoint, initValue, f);
}
std::vector<double> SolverProxy::derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f4p> f) {
    return proxy->derivate(initPoint, endPoint, initValue, f);
}
std::vector<double> SolverProxy::derivate(double initPoint, double endPoint, std::vector<double> initValue, std::vector<Solver_if::f5p> f) {
    return proxy->derivate(initPoint, endPoint, initValue, f);
}