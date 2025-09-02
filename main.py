import argparse
from tabulate import tabulate

from reports.average_report import AverageReport
from reports.status_report import StatusReport
from reports.user_agent_report import UserAgentReport
from utils.log_parser import load_lines


REPORTS = {
    "average": AverageReport(),
    "status_code": StatusReport(),
    "user_agent": UserAgentReport(),
}


def print_average(data):
    table = []
    headers = ["Endpoint", "Запросов", "Ср. время (с)"]
    for url, info in data.items():
        table.append([url, info["count"], round(info["avg_time"], 3)])
    return tabulate(table, headers=headers, tablefmt="grid")


def print_status(data):
    table = []
    headers = ["Статус", "Кол-во"]
    for code, count in data.items():
        table.append([code, count])
    return tabulate(table, headers=headers, tablefmt="grid")


def print_user_agents(data):
    table = []
    headers = ["User-Agent", "Кол-во"]
    for ua, count in data.items():
        table.append([ua, count])
    return tabulate(table, headers=headers, tablefmt="grid")


PRINTERS = {
    "average": print_average,
    "status_code": print_status,
    "user_agent": print_user_agents,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, nargs="+", help="Логи для анализа")
    parser.add_argument("--report", required=True, nargs="+", choices=list(REPORTS.keys()) + ["all"])
    parser.add_argument("--date", help="Фильтр по дате (YYYY-MM-DD)")
    args = parser.parse_args()

    lines = list(load_lines(args.file, args.date))

    reports = REPORTS if "all" in args.report else {r: REPORTS[r] for r in args.report}

    for name, report in reports.items():
        data = report.generate(lines)
        if data:
            print(PRINTERS[name](data))


if __name__ == "__main__":
    main()
