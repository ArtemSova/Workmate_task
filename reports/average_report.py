"""
Модуль отчета по среднему времени ответа endpoint'ов.

Этот модуль предоставляет класс AverageReport для анализа
среднего времени ответа различных URL endpoint'ов на основе логов.
"""

from collections import defaultdict
from utils.log_parser import _try_parse_json
from .base import BaseReport


class AverageReport(BaseReport):
    """
    Класс для генерации отчета по среднему времени ответа endpoint'ов.

    Наследуется от BaseReport и реализует метод generate() для анализа
    среднего времени ответа различных URL на основе логов веб-сервера.

    Attributes:
        Нет публичных атрибутов

    Methods:
        generate(lines): Генерирует отчет со статистикой по URL


    Использование:
        from reports.average_report import AverageReport
        report = AverageReport()
        data = report.generate(parsed_lines)
    """

    def generate(self, lines):
        """
        Анализирует логи и вычисляет среднее время ответа для каждого URL.

        Обрабатывает каждую строку лога, извлекает URL и время ответа,
        агрегирует статистику и вычисляет средние значения.

        Args:
            lines (list): Список строк логов. Каждая строка может быть:
                         - JSON-строкой для парсинга
                         - Уже распарсенным словарем

        Returns:
            dict: Словарь с статистикой по каждому URL в формате:
                  {
                      "url": {
                          "count": int,      # Количество запросов
                          "avg_time": float  # Среднее время ответа в секундах
                      }
                  }

        Notes:
            - Пропускает строки, которые не удается распарсить
            - Игнорирует записи с некорректным временем ответа
            - Использует defaultdict для автоматической инициализации статистики
        """

        # Инициализация словаря со статистикой с автоматической инициализацией
        stats = defaultdict(lambda: {"count": 0, "total_time": 0.0})

        # Обработка каждой строки лога
        for line in lines:
            # Парсинг JSON или использование готового словаря
            obj = _try_parse_json(line)
            if not obj:
                continue

            # Извлечение URL и времени ответа
            url = obj.get("url")
            rt = obj.get("response_time")

            # Проверка наличия обязательных полей
            if url and rt is not None:
                try:
                    # Конвертация времени ответа в float и обновление статистики
                    rt = float(rt)
                    stats[url]["count"] += 1
                    stats[url]["total_time"] += rt
                except ValueError:
                    # Пропуск записей с некорректным временем ответа
                    continue

        # Вычисление средних значений для каждого URL
        result = {}
        for url, data in stats.items():
            result[url] = {
                "count": data["count"],
                "avg_time": data["total_time"] / data["count"]
            }
        return result
