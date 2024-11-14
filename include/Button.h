#ifndef BUTTON_HPP
#define BUTTON_HPP

#include <SFML/Graphics.hpp>
#include <string>

// Базовый класс для кнопок
class Button {
public:
    // Конструктор для кнопки
    Button(float x, float y, float width, float height, const std::string& label);
    
    // Чисто виртуальная функция для обработки кликов (будет реализована в дочерних классах)
    virtual void handleClick(sf::Vector2f mousePos) = 0;
    
    // Метод для рисования кнопки на экране
    void draw(sf::RenderWindow& window);
    
    bool getStaus();
protected:
    sf::RectangleShape buttonShape;  // Прямоугольник, представляющий кнопку
    sf::Text labelText;              // Текст кнопки
    sf::Font font;                   // Шрифт для текста
    
};

// Класс для переключаемой кнопки
class ToggleButton : public Button {
public:
    ToggleButton(float x, float y, float width, float height, const std::string& label);
    
    // Реализация обработки клика
    void handleClick(sf::Vector2f mousePos) override;

    bool getStaus();
private:
    bool isActive;  // Флаг, показывающий активен ли статус кнопки
};

// Класс для кликающей кнопки
class ClickButton : public Button {
public:
    ClickButton(float x, float y, float width, float height, const std::string& label);
    
    // Реализация обработки клика
    void handleClick(sf::Vector2f mousePos) override;

    bool getStaus();
private:
    bool isClicked;  // Флаг, показывающий, была ли кнопка нажата
};

#endif // BUTTON_HPP
