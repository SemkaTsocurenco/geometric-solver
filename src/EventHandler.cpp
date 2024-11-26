#include "../include/EventHandler.h"
#include "../include/events.h"


EventHandler::EventHandler(std::vector<Point>& points, std::vector<Point*>& selectedPoints, std::vector<Line>& lines,
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
            if (line.startPoint->position == draggedPoint->position)  {
                line.startPoint->position = cursorPosition;
            } else if(line.endPoint->position == draggedPoint->position) {
                line.endPoint->position = cursorPosition;
            }
        }
        draggedPoint->position = cursorPosition;
    }

    if (dragLine != nullptr && buttons.MoveLineModeButton.getStaus()) {
        sf::Vector2f offset = cursorPosition - draggedPoint->position;
        dragLine->startPoint->position = startLine[0].position + offset;
        dragLine->endPoint->position = startLine[1].position + offset;
        draggedPointLineStart->position = dragLine->startPoint->position;
        draggedPointLineEnd->position = dragLine->endPoint->position;
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

    if (buttons.DrawLineButton.getStaus()) {    
        buttons.DrawLineButton.setPressed(true);
        draw_line(lines, selectedPoints, false);
        return;
    }
    buttons.DrawLineButton.setPressed(false);



    if (buttons.MovePointModeButton.getStaus()) {
        buttons.DrawLineModeButton.isActive = false;
        buttons.MoveLineModeButton.isActive = false;
        MovePointMode(points, event, draggedPoint);
        return;
    }

    if (buttons.MoveLineModeButton.getStaus()){
        buttons.DrawLineModeButton.isActive = false;
        buttons.MovePointModeButton.isActive = false;
        MoveLineMode(points, lines, event,
                    draggedPoint, draggedPointLineStart,
                    draggedPointLineEnd,
                    startLine, dragLine);
        return;
    }

    if (event.mouseButton.button == sf::Mouse::Left) {
        draw_point(points, selectedPoints, event);

    } else if (event.mouseButton.button == sf::Mouse::Right && selectedPoints.size() >= 2) {
        draw_line(lines, selectedPoints, true);
    }

    if (buttons.DrawLineModeButton.getStaus()) {
        buttons.MovePointModeButton.isActive = false;
        buttons.MoveLineModeButton.isActive = false;
        draw_line(lines, selectedPoints, false);
    }
}

void EventHandler::handleKeyboardPress(const sf::Event& event) {
    if (event.key.code == sf::Keyboard::C) {

    }
}

void EventHandler::handleWindowClose(const sf::Event& event, sf::RenderWindow& window) {
    window.close();
}