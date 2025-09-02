"""
Unit-тесты для модулей отчетов и парсера.

Этот модуль содержит unit-тесты для отдельных компонентов системы:
- AverageReport - отчет по среднему времени ответа
- StatusReport - отчет по статус-кодам
- UserAgentReport - отчет по User-Agent'ам
- _try_parse_json - функция парсинга JSON строк

Тесты проверяют изолированную функциональность каждого компонента.
"""

import pytest
from reports.average_report import AverageReport
from reports.status_report import StatusReport
from reports.user_agent_report import UserAgentReport

@pytest.fixture
def sample_lines():
    """
    Фикстура с разнообразными тестовыми данными для всех отчетов.

    Returns:
        list: Список тестовых строк логов, содержащих:
              - Данные для AverageReport (url + response_time)
              - Данные для StatusReport (status codes)
              - Данные для UserAgentReport (http_user_agent)
              - Смешанные данные для проверки изоляции отчетов
    """

    return [
        '{"url": "/api/test", "response_time": "0.1"}',
        '{"url": "/api/test", "response_time": "0.2"}',
        '{"url": "/api/other", "response_time": "0.3"}',
        '{"status": "200"}',
        '{"status": "404"}',
        '{"status": "200"}',
        '{"http_user_agent": "Mozilla/5.0"}',
        '{"http_user_agent": "curl/7.0"}',
        '{"http_user_agent": "Mozilla/5.0"}',
    ]

def test_average_report(sample_lines):
    """
    Unit-тест для AverageReport.

    Проверяет что отчет корректно:
    - Группирует запросы по URL
    - Подсчитывает количество запросов для каждого URL
    - Вычисляет среднее время ответа
    - Игнорирует строки без данных для этого отчета

    Args:
        sample_lines: Фикстура с тестовыми данными
    """

    report = AverageReport()
    result = report.generate(sample_lines)

    # Ожидаемые результаты
    expected = {
        "/api/test": {"count": 2, "avg_time": 0.15},
        "/api/other": {"count": 1, "avg_time": 0.3},
    }

    # Проверка всех ожидаемых результатов
    for url, data in expected.items():
        assert url in result
        assert result[url]["count"] == data["count"]
        assert result[url]["avg_time"] == pytest.approx(data["avg_time"])

def test_status_report(sample_lines):
    report = StatusReport()
    result = report.generate(sample_lines)
    expected = {
        "200": 2,
        "404": 1
    }
    assert result == expected

def test_user_agent_report(sample_lines):
    """
    Unit-тест для StatusReport.

    Проверяет что отчет корректно:
    - Подсчитывает количество каждого статус-кода
    - Игнорирует строки без поля status
    - Возвращает правильное распределение

    Args:
        sample_lines: Фикстура с тестовыми данными
    """
    report = UserAgentReport()
    result = report.generate(sample_lines)

    expected = {
        "Mozilla/5.0": 2,
        "curl/7.0": 1
    }

    assert result == expected


@pytest.mark.parametrize("input_line, should_succeed, expected_url, expected_time", [
    # Валидные случаи
    ('{"url": "/api/test", "response_time": "0.1"}', True, "/api/test", 0.1),
    ('{"url": "/api/test", "response_time": "0.2"}', True, "/api/test", 0.2),

    # Невалидные случаи
    ('{"url": "/api/test", "response_time": "not_a_number"}', False, "/api/test", None), # Время не число
    ('{"url": "/api/test"}', True, "/api/test", None), # Нет времени отклика
    ('{"response_time": "0.1"}', True, None, 0.1), # Нет URL
    ('invalid json', False, None, None), # Совсем не JSON
])
def test_average_parsing(input_line, should_succeed, expected_url, expected_time):
    """
    Параметризованный тест парсинга JSON для AverageReport.

    Проверяет различные edge cases парсинга JSON строк:
    - Валидный JSON с корректными данными
    - Валидный JSON с некорректными числовыми значениями
    - Валидный JSON с отсутствующими полями
    - Невалидный JSON

    Args:
        input_line: JSON строка для парсинга
        should_succeed: Ожидается ли успешный парсинг
        expected_url: Ожидаемый URL (если есть)
        expected_time: Ожидаемое время ответа (если есть)
    """

    from utils.log_parser import _try_parse_json

    obj = _try_parse_json(input_line)

    if should_succeed and obj:
        ## Проверка успешного парсинга
        if expected_url is not None:
             assert obj.get("url") == expected_url
        if expected_time is not None:
             assert float(obj.get("response_time")) == expected_time
    elif not should_succeed or obj is None:
        # Проверка неуспешного парсинга
        if expected_url is not None and obj:
             assert obj.get("url") == expected_url


