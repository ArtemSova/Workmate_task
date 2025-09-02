"""
Анализатор логов веб-сервера

Этот скрипт анализирует логи веб-сервера и генерирует различные типы отчетов
в удобном табличном формате.

Использование:
    python main.py --file <файлы> --report <типы_отчетов> [--date <дата>]

Аргументы:
    --file      Один или несколько файлов логов (обязательный)
    --report    Тип отчета: average, status_code, user_agent или all (обязательный)
    --date      Фильтр по дате в формате YYYY-MM-DD (опционально)

Доступные отчеты:
    average     - Среднее время ответа по endpoint'ам
    status_code - Распределение HTTP статус-кодов
    user_agent  - Распределение User-Agent'ов

Модули:
    reports.average_report   - Отчет по среднему времени ответа
    reports.status_report    - Отчет по кодам статуса
    reports.user_agent_report - Отчет по User-Agent'ам
    utils.log_parser         - Парсер логов

Примеры использования:

- Базовые примеры:
    python main.py --file access.log --report average
    python main.py --file access.log --report user_agent
    python main.py --file access.log --report status_code

- С фильтрацией по дате:
    python main.py --file access.log --report average --date 2025-06-22
    python main.py --file access.log --report status_code --date 2021-01-01

- С несколькими файлами:
    python main.py --file access.log error.log --report average
    python main.py --file access.log error.log --report all --date 2025-06-22

Запуск тестов:
    python -m pytest tests/ -v
"""

import argparse
from tabulate import tabulate

from reports.average_report import AverageReport
from reports.status_report import StatusReport
from reports.user_agent_report import UserAgentReport
from utils.log_parser import load_lines


# Словарь доступных отчетов (расширять при создании новых классов отчетов)
REPORTS = {
    "average": AverageReport(),
    "status_code": StatusReport(),
    "user_agent": UserAgentReport(),
}


def print_average(data):
    """
    Формирует таблицу с данными о среднем времени ответа.

    Args:
        data (dict): Словарь с данными в формате {url: {"count": int, "avg_time": float}}

    Returns:
        str: Отформатированная таблица в виде строки
    """
    table = []
    headers = ["Endpoint", "Запросов", "Ср. время (с)"]
    for url, info in data.items():
        table.append([url, info["count"], round(info["avg_time"], 3)])
    return tabulate(table, headers=headers, tablefmt="grid")


def print_status(data):
    """
    Формирует таблицу со статистикой кодов статуса.

    Args:
        data (dict): Словарь с данными в формате {status_code: count}

    Returns:
        str: Отформатированная таблица в виде строки
        """
    table = []
    headers = ["Статус", "Кол-во"]
    for code, count in data.items():
        table.append([code, count])
    return tabulate(table, headers=headers, tablefmt="grid")


def print_user_agents(data):
    """
    Формирует таблицу с количественной статистикой User-Agent'ов.

    Args:
        data (dict): Словарь с данными в формате {user_agent: count}

    Returns:
        str: Отформатированная таблица в виде строки
    """
    table = []
    headers = ["User-Agent", "Кол-во"]
    for ua, count in data.items():
        table.append([ua, count])
    return tabulate(table, headers=headers, tablefmt="grid")

# Словарь функций форматирования для каждого типа отчета
# (расширять при создании новых классов отчетов)
PRINTERS = {
    "average": print_average,
    "status_code": print_status,
    "user_agent": print_user_agents,
}


def main():
    """
    Основная функция программы.

    Обрабатывает аргументы командной строки, загружает логи,
    генерирует отчеты и выводит результаты.
    """
    parser = argparse.ArgumentParser(
        description="Анализатор логов веб-сервера",
        epilog="Пример: python main.py --file my_logs.log --report all"
    )
    parser.add_argument(
        "--file",
        required=True,
        nargs="+",
        help="Один или несколько файлов логов для анализа"
    )
    parser.add_argument(
        "--report",
        required=True,
        nargs="+",
        choices=list(REPORTS.keys()) + ["all"],
        help="Тип отчета: average, status_code, user_agent или all"
    )
    parser.add_argument(
        "--date",
        help="Фильтр по дате в формате YYYY-MM-DD"
    )
    args = parser.parse_args()

    # Загрузка и парсинг строк логов
    lines = list(load_lines(args.file, args.date))

    # Выбор отчетов для генерации
    reports = REPORTS if "all" in args.report else {r: REPORTS[r] for r in args.report}

    # Генерация и вывод отчетов
    for name, report in reports.items():
        data = report.generate(lines)
        if data:
            print(f"\nОтчет: {name}")
            print("-" * 60)
            print(PRINTERS[name](data))
            print()


if __name__ == "__main__":
    main()
