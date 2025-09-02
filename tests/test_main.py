"""
Интеграционные тесты для модуля main и отчетов.

Этот модуль содержит интеграционные тесты, которые проверяют
взаимодействие между компонентами системы: отчетами, генерацией
данных и форматированием выводов.

Тесты проверяют, что:
1. Отчеты корректно генерируют данные из входных строк
2. Принтеры правильно форматируют данные в таблицы
3. Весь pipeline от данных до вывода работает корректно

Используется фикстура для создания mock-данных логов.
"""

import pytest
from main import REPORTS, PRINTERS


@pytest.fixture
def mock_lines():
    """
    Фикстура с тестовыми данными логов в JSON формате.

    Returns:
        list: Список строк логов с различными данными для тестирования:
              - Два запроса к одному URL с разным временем ответа
              - Разные статус-коды (200 и 404)
              - Разные User-Agent строки
              - Валидный JSON формат
    """

    return [
        '{"url": "/api/test", "response_time": "0.1", "status": "200", "http_user_agent": "Mozilla"}',
        '{"url": "/api/test", "response_time": "0.2", "status": "404", "http_user_agent": "curl"}',
    ]

def test_average_report_integration(mock_lines):
    """
    Интеграционный тест для отчета по среднему времени ответа.

    Проверяет полный pipeline: генерация данных + форматирование вывода.
    Убеждается, что:
    - Отчет генерирует корректные данные из входных строк
    - Принтер создает таблицу с правильными заголовками
    - Данные содержат правильные вычисленные значения

    Args:
        mock_lines: Фикстура с тестовыми данными логов
    """

    report = REPORTS["average"]
    printer = PRINTERS["average"]

    # Генерация данных отчетом
    data = report.generate(mock_lines)

    # Форматирование данных принтером
    output = printer(data)

    # Проверка заголовков таблицы
    assert "Endpoint" in output
    assert "Запросов" in output
    assert "Ср. время (с)" in output

    # Проверка наличия данных в выводе
    assert "/api/test" in output
    assert "2" in output  # Количество запросов

    # Проверка вычисления среднего времени
    lines = output.split('\n')
    relevant_line = next((line for line in lines if '/api/test' in line), None)
    assert relevant_line is not None
    assert "0.15" in relevant_line  # (0.1 + 0.2) / 2 = 0.15


def test_status_report_integration(mock_lines):
    """
    Интеграционный тест для отчета по статус-кодам.

    Проверяет, что отчет по статус-кодам корректно:
    - Подсчитывает количество каждого статус-кода
    - Форматирует вывод в таблицу с правильными заголовками
    - Содержит все ожидаемые статус-коды и их количество

    Args:
        mock_lines: Фикстура с тестовыми данными логов
    """

    report = REPORTS["status_code"]
    printer = PRINTERS["status_code"]

    data = report.generate(mock_lines)
    output = printer(data)

    # Проверка заголовков таблицы (с учетом возможного форматирования)
    assert "Статус" in output or "Ста́тус" in output
    assert "Кол-во" in output

    # Проверка наличия всех статус-кодов
    assert "200" in output
    assert "404" in output

    # Проверка корректного подсчета
    assert "1" in output  # Каждый статус-код встречается 1 раз

def test_user_agent_report_integration(mock_lines):
    """
    Интеграционный тест для отчета по User-Agent.

    Проверяет, что отчет по User-Agent корректно:
    - Подсчитывает количество каждого User-Agent
    - Форматирует вывод в таблицу с правильными заголовками
    - Содержит все ожидаемые User-Agent строки и их количество

    Args:
        mock_lines: Фикстура с тестовыми данными логов
    """

    report = REPORTS["user_agent"]
    printer = PRINTERS["user_agent"]

    data = report.generate(mock_lines)
    output = printer(data)

    # Проверка заголовков таблицы
    assert "User-Agent" in output
    assert "Кол-во" in output

    # Проверка наличия всех User-Agent строк
    assert "Mozilla" in output
    assert "curl" in output

    # Проверка корректного подсчета
    assert "1" in output  # Каждый User-Agent встречается 1 раз
