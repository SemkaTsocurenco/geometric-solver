#pragma once
#include "Point.h"

class Line {
public:
    Point startPoint;
    Point endPoint;

    Line(Point start, Point end)
        : startPoint(start), endPoint(end) {}

    void draw(sf::RenderWindow& window) const {
        sf::VertexArray line(sf::Lines, 2);
        line[0].position = startPoint.position;
        line[1].position = endPoint.position;
        line[0].color = sf::Color::Black;
        line[1].color = sf::Color::Black;
        window.draw(line);
    }
};
