#include "PDProxy.h"
#include "ProbabilityDistributionStudent.h"

#include <stdlib.h>
#include <iostream>

using namespace std;

unsigned int PDProxy::_maxRecursions = 100;
void PDProxy::setMaxRecursions (unsigned int maxRecursions) {
    _maxRecursions = maxRecursions;
}

unsigned int PDProxy::getMaxRecursions() {
    return _maxRecursions;
}

unsigned int PDProxy::_count = 0;
void PDProxy::setCount(unsigned int count) {
    _count = count;
}
unsigned int PDProxy::getCount() {
    return _count;
}

double PDProxy::inverseChi2(double cumulativeProbability, double degreeFreedom) {
    return ProbabilityDistributionStudent::inverseChi2(cumulativeProbability, degreeFreedom);
}

double PDProxy::inverseFFisherSnedecor(double cumulativeProbability, double d1, double d2) {
    return ProbabilityDistributionStudent::inverseFFisherSnedecor(cumulativeProbability, d1, d2);
}

double PDProxy::inverseNormal(double cumulativeProbability, double mean, double stddev) {
    return ProbabilityDistributionStudent::inverseNormal(cumulativeProbability, mean, stddev);
}

double PDProxy::inverseTStudent(double cumulativeProbability, double mean, double stddev, double degreeFreedom) {
    return ProbabilityDistributionStudent::inverseTStudent(cumulativeProbability, mean, stddev, degreeFreedom);
}

double PDProxy::findInverseChi2(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double degreeFreedom) {
    _count++;
    cout << "findInversechi2("<< a << ", " << b << ")" << endl;
    return ProbabilityDistributionStudent::findInverseChi2(a, fa, b, fb, recursions, cumulativeProbability, degreeFreedom);
}

double PDProxy::findInverseFFisherSnedecor(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double d1, double d2) {
    _count++;
    cout << "findInverseFFisherSnedecor(" << a << ", " << b << ")" << endl;
    return ProbabilityDistributionStudent::findInverseFFisherSnedecor(a, fa, b, fb, recursions, cumulativeProbability, d1, d2);
}

double PDProxy::findInverseNormal(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev) {
    _count++;
    cout << "findInverseNormal ("<< a <<", "<< b << "J" << endl;
    return ProbabilityDistributionStudent::findInverseNormal(a, fa, b, fb, recursions, cumulativeProbability, mean, stddev);
}

double PDProxy::findInverseTStudent(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev, double degreeFreedom) {
    _count++;
    cout << "findInverseTStudent(" << a << ", " << b << ")" << endl;
    return ProbabilityDistributionStudent::findInverseTStudent(a, fa, b, fb, recursions, cumulativeProbability, mean, stddev, degreeFreedom);
}