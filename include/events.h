


void draw_point(std::vector<Point>& points, std::vector<Point>& selectedPoints, const sf::Event& event){
    // Check for selecting or creating points
    for (size_t i = 0; i < points.size(); i++) {
        if ((std::abs(event.mouseButton.x - points[i].position.x) <= 8) &&
            (std::abs(event.mouseButton.y - points[i].position.y) <= 8)) {
            selectedPoints.emplace_back(Point(points[i].position.x, points[i].position.y, true, i));
            if (selectedPoints.size() == 3) {
                selectedPoints = {selectedPoints[1], selectedPoints[2]};
            }
            return;
        }
    }

    // Create new point if none selected
    points.emplace_back(event.mouseButton.x, event.mouseButton.y, false);
    selectedPoints.emplace_back(Point(event.mouseButton.x, event.mouseButton.y, true, points.size() - 1));
    if (selectedPoints.size() == 3) {
        selectedPoints = {selectedPoints[1], selectedPoints[2]};
    }
}

void draw_line(std::vector<Line>& lines, std::vector<Point>& selectedPoints, bool clearSelected){
    if (selectedPoints.size() == 2) {
        lines.emplace_back(selectedPoints[0], selectedPoints[1]);
    }
    if (clearSelected) selectedPoints.clear();
}


void draw_mouse_line(Line& mouseLine, std::vector<Point>& selectedPoints, sf::Vector2f& mousePos, bool ModFlag){
    if (ModFlag){
        if (selectedPoints.size() != 0 ){
            mouseLine = Line(*selectedPoints.end(), Point(mousePos.x, mousePos.y));
        }
    } else {
        mouseLine = Line(Point(0,0), Point(0,0));
    }
}


void move_Point(std::vector<Point>& points, std::vector<Line>& lines, Point* draggedPoint, const sf::Event& event ){
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    for (auto& point : points) {
        if ((std::abs(mousePos.x - point.position.x) <= 8) &&
            (std::abs(mousePos.y - point.position.y) <= 8)) {
            draggedPoint = &point; // Устанавливаем перетаскиваемую точку
            return;
        }
    }

    // for (auto& Line : lines)
}
