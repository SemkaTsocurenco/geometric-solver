


void draw_point(std::vector<Point>& points, std::vector<Point*>& selectedPoints, const sf::Event& event){
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


Line* MovableLine( std::vector<Line>& lines, const sf::Event& event){
    int i = 0;
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    for (auto& line : lines){
        i++;
        float dx = line.endPoint->position.x - line.startPoint->position.x;
        float dy = line.endPoint->position.y - line.startPoint->position.y;
        float numerator = std::abs(dy * mousePos.x - dx * mousePos.y + line.endPoint->position.x * line.startPoint->position.y - line.endPoint->position.y * line.startPoint->position.x);
        float denominator = std::sqrt(dx * dx + dy * dy);
        float distance = numerator / denominator;
        if (distance <= 10) {
            float dot1 = (mousePos.x - line.startPoint->position.x) * dx + (mousePos.y - line.startPoint->position.y) * dy;
            float dot2 = (mousePos.x - line.endPoint->position.x) * -dx + (mousePos.y - line.endPoint->position.y) * -dy;
            if (dot1 >= 0 && dot2 >= 0) return &line;
        }
    }
    return nullptr;
}


void MovePointMode(std::vector<Point>& points, const sf::Event& event, Point*& draggedPoint){
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    for (auto& point : points) {
        if ((std::abs(mousePos.x - point.position.x) <= 8) &&
            (std::abs(mousePos.y - point.position.y) <= 8)) {
            draggedPoint = &point; 
            return;
        } 
    }
    return;
}

void MoveLineMode(std::vector<Point>& points,
                  std::vector<Line>& lines,
                  const sf::Event& event,
                  Point*& draggedPoint,
                  Point*& draggedPointLineStart,
                  Point*& draggedPointLineEnd,
                  std::vector<Point>& startLine,
                  Line*& dragLine
                  ){
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    dragLine = MovableLine(lines, event);
    if (dragLine != nullptr){
        startLine[0] = *dragLine->startPoint;
        startLine[1] = *dragLine->endPoint;
        draggedPoint = new Point(0,0);
        draggedPoint->position = mousePos;

        for (auto& point : points){
            if (dragLine->startPoint->position == point.position){
                draggedPointLineStart =  &point;
            } 
            if (dragLine->endPoint->position == point.position){
                draggedPointLineEnd =  &point;
            } 
        }        
    }
    return;
}

