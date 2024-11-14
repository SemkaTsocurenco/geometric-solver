#include "../include/Button.h"
#include <iostream>

// Конструктор базового класса Button
Button::Button(float x, float y, float width, float height, const std::string& label)
    : buttonShape(sf::Vector2f(width, height)) {
    
    buttonShape.setPosition(x, y);
    buttonShape.setFillColor(sf::Color::Blue);

    if (!font.loadFromFile("arial.ttf")) {
        std::cerr << "Ошибка загрузки шрифта!" << std::endl;
    }

    labelText.setFont(font);
    labelText.setString(label);  // Используем переданный текст
    labelText.setCharacterSize(24);
    labelText.setFillColor(sf::Color::White);
    labelText.setPosition(x + width / 2 - labelText.getGlobalBounds().width / 2,
                          y + height / 2 - labelText.getGlobalBounds().height / 2);
}

// Метод для рисования кнопки
void Button::draw(sf::RenderWindow& window) {
    window.draw(buttonShape);
    window.draw(labelText);
}

bool ToggleButton::getStaus(){
    return isActive;
}

// Конструктор для ToggleButton
ToggleButton::ToggleButton(float x, float y, float width, float height, const std::string& label)
    : Button(x, y, width, height, label), isActive(false) {}

// Обработка кликов для ToggleButton
void ToggleButton::handleClick(sf::Vector2f mousePos) {
    if (buttonShape.getGlobalBounds().contains(mousePos.x, mousePos.y)) {
        isActive = !isActive;  // Переключаем состояние
        std::cout << "Состояние ToggleButton: " << (isActive ? "Включено" : "Выключено") << std::endl;
        buttonShape.setFillColor(isActive ? sf::Color::Green : sf::Color::Blue);  // Меняем цвет
    }
}

// Конструктор для ClickButton
ClickButton::ClickButton(float x, float y, float width, float height, const std::string& label)
    : Button(x, y, width, height, label), isClicked(false) {}

// Обработка кликов для ClickButton
void ClickButton::handleClick(sf::Vector2f mousePos) {
    if (buttonShape.getGlobalBounds().contains(mousePos.x, mousePos.y)) {
        isClicked = !isClicked;  // Меняем состояние кнопки
        std::cout << "Кнопка ClickButton " << (isClicked ? "нажата" : "отпущена") << std::endl;
        buttonShape.setFillColor(isClicked ? sf::Color::Red : sf::Color::Blue);  // Меняем цвет
    }
}

bool ClickButton::getStaus(){
    return isClicked;
}