import pytest
from main import REPORTS, PRINTERS


@pytest.fixture
def mock_lines():
    return [
        '{"url": "/api/test", "response_time": "0.1", "status": "200", "http_user_agent": "Mozilla"}',
        '{"url": "/api/test", "response_time": "0.2", "status": "404", "http_user_agent": "curl"}',
    ]

def test_average_report_integration(mock_lines):
    report = REPORTS["average"]
    printer = PRINTERS["average"]
    data = report.generate(mock_lines)
    output = printer(data)
    assert "Endpoint" in output
    assert "Запросов" in output
    assert "Ср. время (с)" in output
    assert "/api/test" in output
    assert "2" in output
    lines = output.split('\n')
    relevant_line = next((line for line in lines if '/api/test' in line), None)
    assert relevant_line is not None
    assert "0.15" in relevant_line

def test_status_report_integration(mock_lines):
    report = REPORTS["status_code"]
    printer = PRINTERS["status_code"]
    data = report.generate(mock_lines)
    output = printer(data)
    assert "Статус" in output or "Ста́тус" in output
    assert "Кол-во" in output
    assert "200" in output
    assert "404" in output
    assert "1" in output

def test_user_agent_report_integration(mock_lines):
    report = REPORTS["user_agent"]
    printer = PRINTERS["user_agent"]
    data = report.generate(mock_lines)
    output = printer(data)
    assert "User-Agent" in output
    assert "Кол-во" in output
    assert "Mozilla" in output
    assert "curl" in output
    assert "1" in output
