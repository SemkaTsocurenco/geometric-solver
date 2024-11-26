#ifndef EVENTHANDLER_H
#define EVENTHANDLER_H

#include <SFML/Graphics.hpp>
#include <vector>
#include <iostream>
#include <cmath>
#include "../include/Point.h"
#include "../include/Line.h"
#include "../include/Constraint.h"
#include "../include/Solver.h"
#include "../include/Button.h"

class EventHandler {
private:
    std::vector<Point>& points;
    std::vector<Point*>& selectedPoints;
    std::vector<Line>& lines;
    Line& mouseLine;
    Point* draggedPoint = nullptr; // Указатель на перетаскиваемую точку
    Point* draggedPointLineStart = nullptr; // Указатель на перетаскиваемую точку
    Point* draggedPointLineEnd = nullptr; // Указатель на перетаскиваемую точку

    Line* dragLine = nullptr;


public:
    EventHandler(std::vector<Point>& points, std::vector<Point*>& selectedPoints, std::vector<Line>& lines,
                 Buttons buttons, Line& mouseLine);

    void processEvent(const sf::Event& event, sf::RenderWindow& window);
    Buttons buttons;
    std::vector<Point> startLine = {Point(0,0), Point(0,0)};


private:
    
    void handleMousePress(const sf::Event& event);
    void handleKeyboardPress(const sf::Event& event);
    void handleWindowClose(const sf::Event& event, sf::RenderWindow& window);
    void handleMouseRealise(const sf::Event& event);
    void handleMouseMoved(const sf::Event& event);

};

#endif // EVENTHANDLER_H