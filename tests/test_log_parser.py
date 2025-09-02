import pytest
from utils.log_parser import _try_parse_json, load_lines
import tempfile
import os


@pytest.fixture
def temp_log_file():
    log_data = (
        '{"@timestamp": "2025-06-22T13:57:32+00:00", "status": 200, "url": "/api/test", "response_time": 0.05}\n'
        '{"@timestamp": "2025-06-23T10:00:00+00:00", "status": 404, "url": "/api/missing", "response_time": 0.1}\n'
        'invalid json line\n'
        '{"@timestamp": "2025-06-22T14:00:00+00:00", "status": 500, "url": "/api/error", "response_time": 0.2}\n'
    )
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(log_data)
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

def test_try_parse_json_valid():
    line = '{"key": "value"}'
    result = _try_parse_json(line)
    assert result == {"key": "value"}

def test_try_parse_json_invalid():
    line = 'invalid json'
    result = _try_parse_json(line)
    assert result is None

def test_load_lines_no_filter(temp_log_file):
    lines = list(load_lines([temp_log_file]))
    assert len(lines) == 4

def test_load_lines_with_date_filter(temp_log_file):
    lines = list(load_lines([temp_log_file], filter_date="2025-06-22"))
    assert len([l for l in lines if '"@timestamp": "2025-06-22' in l]) == 2

def test_load_lines_with_date_filter_excludes_others(temp_log_file):
    lines = list(load_lines([temp_log_file], filter_date="2025-06-22"))
    assert not any('"@timestamp": "2025-06-23' in line for line in lines)
    assert sum(1 for line in lines if '"@timestamp": "2025-06-22' in line) == 2
    assert len(lines) == 2

def test_load_lines_no_filter_correct(temp_log_file):
    lines = list(load_lines([temp_log_file]))
    assert len(lines) == 4





