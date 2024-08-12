#include "DAProxy.h"
#include "DataAnalyserStudent.h"

DAProxy::DAProxy() {
}

std::vector<double> DAProxy::movingAverage(unsigned int n, unsigned short k) {
    DataAnalyserStudent* da = new DataAnalyserStudent();
    return da->movingAverage(n, k);
}

double DAProxy::getDatum(unsigned int i) {
    _count[i]++;
    return _data[i];
}

unsigned int DAProxy::getCount(unsigned int i) {
    return _count[i];
}

void DAProxy::setDatum(unsigned int i, double value) {
    _data[i] = value;
}

double DAProxy::_data[] = {0.0};

unsigned int DAProxy::_count[] = {0};