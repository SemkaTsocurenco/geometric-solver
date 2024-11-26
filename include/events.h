


void draw_point(std::vector<Point>& points, std::vector<Point*>& selectedPoints, const sf::Event& event){
    // Check for selecting or creating points

    for (size_t i = 0; i < points.size(); i++) {
        if ((std::abs(event.mouseButton.x - points[i].position.x) <= 8) &&
            (std::abs(event.mouseButton.y - points[i].position.y) <= 8)) {
            selectedPoints.emplace_back(&points[i]);

            if (selectedPoints.size() == 3) {
                selectedPoints = {selectedPoints[1], selectedPoints[2]};
            }
            for (auto& sp : points){
                sp.isFixed = false;
            }
            for (auto sp : selectedPoints){
                sp->isFixed = true;
            }
            return;
        }
    }

    // Create new point if none selected
    points.push_back(Point(event.mouseButton.x, event.mouseButton.y, false));
    if (points.size() > 2){
        selectedPoints.resize(2);
        selectedPoints[0] = (&points.back()-1);
        selectedPoints[1] = (&points.back());
    }

    if (selectedPoints.size() == 3) {
        selectedPoints = {selectedPoints[1], selectedPoints[2]};
    }
    for (auto& sp : points){
        sp.isFixed = false;

    }
    for (auto& sp : selectedPoints){
        sp->isFixed = true;
    }
}

void draw_line(std::vector<Line>& lines, std::vector<Point*>& selectedPoints, bool clearSelected){
    if (selectedPoints.size() == 2) {
        lines.emplace_back(selectedPoints[0], selectedPoints[1]);
    }
    if (clearSelected) selectedPoints.clear();
}


void draw_mouse_line(Line& mouseLine, std::vector<Point*>& selectedPoints, sf::Vector2f& mousePos, bool ModFlag){
    if (ModFlag){
        if (selectedPoints.size() != 0 ){
            mouseLine = Line(selectedPoints[selectedPoints.size()-1], new Point(mousePos.x, mousePos.y));
        }
    } else {
        mouseLine = Line(nullptr, nullptr);
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

Line* MovableLine( std::vector<Line>& lines, const sf::Event& event){

    int i = 0;
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    for (auto& line : lines){
        i++;
        float dx = line.endPoint->position.x - line.startPoint->position.x;
        float dy = line.endPoint->position.y - line.startPoint->position.y;
        // Вычисляем расстояние от точки до линии
        float numerator = std::abs(dy * mousePos.x - dx * mousePos.y + line.endPoint->position.x * line.startPoint->position.y - line.endPoint->position.y * line.startPoint->position.x);
        float denominator = std::sqrt(dx * dx + dy * dy);
        float distance = numerator / denominator;
        std::cout<<"line "<< i <<"  " << distance << "\n";
        // Проверяем, находится ли точка в пределах толщины линии
        if (distance <= 10) {
            // // Проверим, находится ли мышь между точками линии
            float dot1 = (mousePos.x - line.startPoint->position.x) * dx + (mousePos.y - line.startPoint->position.y) * dy;
            float dot2 = (mousePos.x - line.endPoint->position.x) * -dx + (mousePos.y - line.endPoint->position.y) * -dy;
            if (dot1 >= 0 && dot2 >= 0) return &line;
        }
    }
    return nullptr;
}