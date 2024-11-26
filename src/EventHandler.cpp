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
}

void EventHandler::handleMouseMoved(const sf::Event& event){
        sf::Vector2f cursorPosition(event.mouseMove.x, event.mouseMove.y);
        draw_mouse_line(mouseLine, selectedPoints, cursorPosition, buttons.DrawLineModeButton.getStaus());
        if (draggedPoint != nullptr) {
            draggedPoint->position = cursorPosition;
        }
        
}

void EventHandler::handleMousePress(const sf::Event& event) {
    sf::Vector2f mousePos(event.mouseButton.x, event.mouseButton.y);

    bool flagToggle = buttons.DrawLineModeButton.getStaus();

    buttons.DrawLineModeButton.handleClick(mousePos);
    buttons.MovePointModeButton.handleClick(mousePos);

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
