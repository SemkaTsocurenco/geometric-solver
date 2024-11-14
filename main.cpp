#include <SFML/Graphics.hpp>
#include "./include/Point.h"
#include "./include/Line.h"
#include "./include/Constraint.h"
#include "./include/Solver.h"
#include "./include/Button.h"


#include <iostream>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Geometric Solver");
    std::vector<Point> points;
	std::vector<Point> SelectedPoints;
	ToggleButton toggleButton(10, 10, 100, 30, "Draw Line mod");
	ClickButton clickButton(10, 60, 100, 30, "Draw Line (ПКМ)");


    std::vector<Line> lines;
    std::vector<Constraint*> constraints;
    Solver solver;

	bool select = false;
	bool flagbutton = false;
    bool isDrawingLine = false;
    int selectedPointIndex = -1;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
			}


            if (event.type == sf::Event::MouseButtonPressed) {
				select = false;
                if (event.mouseButton.button == sf::Mouse::Left) {

					sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
					flagbutton = toggleButton.getStaus();
                    toggleButton.handleClick(mousePos);
					clickButton.handleClick(mousePos);
					if (flagbutton != toggleButton.getStaus()){
						break;
					}

					for (int i = 0 ; i< points.size(); i++) { 
						if ((std::abs(event.mouseButton.x - points[i].position.x) <= 8 ) & (std::abs(event.mouseButton.y - points[i].position.y) <= 8 )){
							SelectedPoints.emplace_back(Point(points[i].position.x, points[i].position.y, true, i));
							if (SelectedPoints.size() == 3){
								SelectedPoints = {SelectedPoints[1] , SelectedPoints[2]};
							}
							select = true;
							break;
						}
					}

					if (!select) {
                 		points.emplace_back(event.mouseButton.x, event.mouseButton.y, false);
						SelectedPoints.emplace_back(Point(event.mouseButton.x, event.mouseButton.y, true, points.size()-1));
							if (SelectedPoints.size() == 3){
								SelectedPoints = {SelectedPoints[1] , SelectedPoints[2]};
						}
					}

                } else if (event.mouseButton.button == sf::Mouse::Right && SelectedPoints.size() >= 2) {
					if (SelectedPoints. size() == 2 ){
                    	lines.emplace_back(SelectedPoints[0], SelectedPoints[1]);
					}
					SelectedPoints.clear();
                } 
				if (toggleButton.getStaus()) {
					if (SelectedPoints. size() == 2 ){
                    	lines.emplace_back(SelectedPoints[0], SelectedPoints[1]);
					}
				}
            }


            if (event.type == sf::Event::KeyPressed && event.key.code == sf::Keyboard::C) {

            }
        }



        window.clear(sf::Color::White);
        for (const auto& line : lines) {
            line.draw(window);
        }
        for (const auto& point : points) {
            point.draw(window);
        }
        for (const auto& point : SelectedPoints) {
            point.draw(window);
        }		
		toggleButton.draw(window);
		clickButton.draw(window);

        window.display();
    }

    return 0;
}
