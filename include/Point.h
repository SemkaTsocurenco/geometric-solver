#pragma once
#include <SFML/Graphics.hpp>

class Point {
public:
    sf::Vector2f position;
    bool isFixed;
    int indexPoint;

    Point(float x, float y, bool fixed = false, int index = 0)
        : position(x, y), isFixed(fixed),  indexPoint(index) {}

    void draw(sf::RenderWindow& window) const {
        sf::CircleShape circle(5);
        circle.setFillColor(isFixed ? sf::Color::Blue : sf::Color::Red);
        circle.setPosition(position.x - 5, position.y - 5);
        window.draw(circle);
    }
};