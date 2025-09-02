import pytest
from reports.average_report import AverageReport
from reports.status_report import StatusReport
from reports.user_agent_report import UserAgentReport

@pytest.fixture
def sample_lines():
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
    report = AverageReport()
    result = report.generate(sample_lines)
    expected = {
        "/api/test": {"count": 2, "avg_time": 0.15},
        "/api/other": {"count": 1, "avg_time": 0.3},
    }

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
    report = UserAgentReport()
    result = report.generate(sample_lines)
    expected = {
        "Mozilla/5.0": 2,
        "curl/7.0": 1
    }
    assert result == expected


@pytest.mark.parametrize("input_line, should_succeed, expected_url, expected_time", [
    ('{"url": "/api/test", "response_time": "0.1"}', True, "/api/test", 0.1),
    ('{"url": "/api/test", "response_time": "0.2"}', True, "/api/test", 0.2),
    ('{"url": "/api/test", "response_time": "not_a_number"}', False, "/api/test", None), # Время не число
    ('{"url": "/api/test"}', True, "/api/test", None), # Нет времени отклика
    ('{"response_time": "0.1"}', True, None, 0.1), # Нет URL
    ('invalid json', False, None, None), # Совсем не JSON
])
def test_average_parsing(input_line, should_succeed, expected_url, expected_time):
    from utils.log_parser import _try_parse_json
    obj = _try_parse_json(input_line)
    if should_succeed and obj:
        if expected_url is not None:
             assert obj.get("url") == expected_url
        if expected_time is not None:
             assert float(obj.get("response_time")) == expected_time
    elif not should_succeed or obj is None:
        if expected_url is not None and obj:
             assert obj.get("url") == expected_url


