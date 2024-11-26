#include "../include/EventHandler.h"
#include "../include/events.h"


EventHandler::EventHandler(std::vector<Point>& points, std::vector<Point>& selectedPoints, std::vector<Line>& lines,
                 Buttons buttons, Line& mouseLine)
    : points(points), selectedPoints(selectedPoints), lines(lines), buttons(buttons), mouseLine(mouseLine){}

void EventHandler::processEvent(const sf::Event& event, sf::RenderWindow& window) {

    switch (event.type) {
        case sf::Event::Closed:
            handleWindowClose(event, window);
            break;
        case sf::Event::MouseButtonPressed:
            handleMousePress(event);
            break;
        case sf::Event::MouseButtonReleased:
            // Возврат кнопки в исходное состояние
            handleMouseRealise(event);
            break;
        case sf::Event::MouseMoved:
            handleMouseMoved(event);
            break;
        case sf::Event::KeyPressed:
            handleKeyboardPress(event);
            break;
        default:
            break;
    }
}

void EventHandler::handleMouseRealise(const sf::Event& event){
        buttons.DrawLineButton.setPressed(false);
            // Сброс указателя перемещаемой точки
        if (event.mouseButton.button == sf::Mouse::Left) {
            draggedPoint = nullptr;
        }
        if (event.mouseButton.button == sf::Mouse::Left) {
            dragLine = nullptr;
        }


}

void EventHandler::handleMouseMoved(const sf::Event& event){
        sf::Vector2f cursorPosition(event.mouseMove.x, event.mouseMove.y);
        draw_mouse_line(mouseLine, selectedPoints, cursorPosition, buttons.DrawLineModeButton.getStaus());
        if (draggedPoint != nullptr && buttons.MovePointModeButton.getStaus()) {
            for (auto& line : lines) {
                if (line.startPoint.position == draggedPoint->position)  {
                    line.startPoint.position = cursorPosition;
                } else if(line.endPoint.position == draggedPoint->position) {
                    line.endPoint.position = cursorPosition;
                }
            }
            draggedPoint->position = cursorPosition;
        }

        if (dragLine != nullptr && buttons.MoveLineModeButton.getStaus()) {
            sf::Vector2f offset = cursorPosition - draggedPoint->position; // Вычисляем смещение
            std::cout<<offset.x << ", "<<offset.y<<"\n\n";
            dragLine->startPoint.position = startLine.startPoint.position + offset;
            dragLine->endPoint.position = startLine.endPoint.position + offset;
            
            draggedPointLineStart->position = dragLine->startPoint.position;
            draggedPointLineEnd->position = dragLine->endPoint.position;
        }
}

void EventHandler::handleMousePress(const sf::Event& event) {
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);
    sf::Vector2f cursorPosition(event.mouseMove.x, event.mouseMove.y);

    bool flagToggle = buttons.DrawLineModeButton.getStaus();

    buttons.DrawLineModeButton.handleClick(mousePos);
    buttons.MovePointModeButton.handleClick(mousePos);
    buttons.MoveLineModeButton.handleClick(mousePos);


    buttons.DrawLineButton.handleClick(mousePos);

    if (flagToggle != buttons.DrawLineModeButton.getStaus()) {
        return;
    }

    // Проверка нажатия на ClickButton
    if (buttons.DrawLineButton.getStaus()) {
        buttons.DrawLineButton.setPressed(true);
        draw_line(lines, selectedPoints, true);
        return;
    }

    // Сбрасываем состояние кнопки
    buttons.DrawLineButton.setPressed(false);

    // Если включен режим перемещения точек
    if (buttons.MovePointModeButton.getStaus()) {
        selectedPoints = {};
        for (auto& point : points) {
            if ((std::abs(mousePos.x - point.position.x) <= 8) &&
                (std::abs(mousePos.y - point.position.y) <= 8)) {
                draggedPoint = &point; // Устанавливаем перетаскиваемую точку
                return;
            } 
        }
        return;
    }

    if (buttons.MoveLineModeButton.getStaus()){
        selectedPoints = {};
        dragLine = MovableLine(lines, event);
        if (dragLine != nullptr){
            startLine.startPoint = dragLine->startPoint;
            startLine.endPoint = dragLine->endPoint;
            draggedPoint = new Point(0,0);
            draggedPoint->position = mousePos;

            for (auto& point : points){
                if (dragLine->startPoint.position == point.position){
                    draggedPointLineStart =  &point;
                } 
                if (dragLine->endPoint.position == point.position){
                    draggedPointLineEnd =  &point;
                } 
            }        
        }
        
        return;
    }



    if (event.mouseButton.button == sf::Mouse::Left) {
        draw_point(points, selectedPoints, event);

    } else if (event.mouseButton.button == sf::Mouse::Right && selectedPoints.size() >= 2) {
        draw_line(lines, selectedPoints, true);
    }
    if (buttons.DrawLineModeButton.getStaus()) {
        draw_line(lines, selectedPoints, false);
    }
}




void EventHandler::handleKeyboardPress(const sf::Event& event) {
    if (event.key.code == sf::Keyboard::C) {
        // Implement constraint handling or other functionality here
    }
}




void EventHandler::handleWindowClose(const sf::Event& event, sf::RenderWindow& window) {
    window.close();
}
