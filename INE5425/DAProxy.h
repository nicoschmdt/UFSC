#ifndef DATAANALYSER_PROXY_H
#define DATAANALYSER_PROXY_H

#include <iostream>
#include <string>
#include <vector>

class DAProxy {
    public:
        DAProxy();
        std::vector<double> movingAverage(unsigned int n, unsigned short k);
        static unsigned int getCount(unsigned int i);
        static double getDatum(unsigned int i);
        static void setDatum(unsigned int i, double value);
        static double _data[100];
        static unsigned int _count[100];
};

#endif /* DATAANALYSER_PROXY_H */