#pragma once
#include <vector>
#include "Point.h"
#include "Line.h"

class Constraint {
public:
    virtual void apply(std::vector<Point>& points) = 0;
};

class CoincidenceConstraint : public Constraint {
private:
    int point1Index;
    int point2Index;

public:
    CoincidenceConstraint(int p1, int p2)
        : point1Index(p1), point2Index(p2) {}

    void apply(std::vector<Point>& points) override {
        points[point2Index].position = points[point1Index].position;
    }
};
