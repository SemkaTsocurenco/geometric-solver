#include "./include/EventHandler.h"
#include <iostream>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Geometric Solver");

    std::vector<Point> points;
    std::vector<Point> selectedPoints;
    std::vector<Line> lines;
    Line mouseLine (Point(0,0), Point(0,0));

    ToggleButton DrawLineModeButton(10, 10, 100, 30, "Draw Line mod");
    ToggleButton MovePointModeButton(10, 60, 100, 30, "Move Point mod");
    ClickButton DrawLineButton(10, 120, 100, 30, "Draw Line (RMB)");

    Buttons buttons {DrawLineModeButton,  MovePointModeButton, DrawLineButton};


    EventHandler eventHandler(points, selectedPoints, lines, buttons, mouseLine);

    while (window.isOpen()) {
        sf::Event event;
        window.clear(sf::Color::White);

        while (window.pollEvent(event)) {
            eventHandler.processEvent(event, window);
        }

        

        for (const auto& line : lines) {
            line.draw(window);
        }
        for (const auto& point : points) {
            point.draw(window);
        }
        for (const auto& point : selectedPoints) {
            point.draw(window);
        }
        DrawLineModeButton.draw(window);
        MovePointModeButton.draw(window);
        DrawLineButton.draw(window);


        mouseLine.draw(window);

        window.display();
    }

    return 0;
}
