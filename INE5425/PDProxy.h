#ifndef PROBABILITYDISTRIBUTIONPROXY_H
#define PROBABILITYDISTRIBUTIONPROXY_H
#include "ProbabilityDistributionBase.h"


class PDProxy : public ProbabilityDistributionBase {
    public:
        static void setMaxRecursions(unsigned int maxRecursions);
        static unsigned int getMaxRecursions();
        static void setCount(unsigned int count);
        static unsigned int getCount();

        static double inverseChi2(double cumulativeProbability, double degreeFreedom);
        static double inverseFFisherSnedecor(double cumulativeProbability, double d1, double d2);
        static double inverseNormal (double cumulativeProbability, double mean, double stddev);
        static double inverseTStudent(double cumulativeProbability, double mean, double stddev, double degreeFreedom);

        static double findInverseChi2(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double degreeFreedom);
        static double findInverseFFisherSnedecor(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double d1, double d2);
        static double findInverseNormal (double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev);
        static double findInverseTStudent(double a, double fa, double b, double fb, unsigned int recursions, double cumulativeProbability, double mean, double stddev, double degreeFreedom);

    private:
        static unsigned int _maxRecursions;
        static unsigned int _count;
};

#endif /* PROBABILITYDISTRIBUTIONPROXY_H */