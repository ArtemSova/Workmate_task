from collections import Counter
from utils.log_parser import _try_parse_json
from .base import BaseReport

class StatusReport(BaseReport):
    """
    Класс для генерации отчета по распределению HTTP статус-кодов.

    Наследуется от BaseReport и реализует метод generate() для анализа
    частоты встречаемости различных HTTP статус-кодов в логах веб-сервера.

    Attributes:
        Нет публичных атрибутов

    Methods:
        generate(lines): Генерирует отчет со статистикой статус-кодов

    Использование:
        from reports.status_report import StatusReport

        report = StatusReport()
        data = report.generate(parsed_lines)
    """

    def generate(self, lines):
        """
        Анализирует логи и подсчитывает количество каждого HTTP статус-кода.

        Обрабатывает каждую строку лога, извлекает статус-код и подсчитывает
        частоту встречаемости каждого кода с помощью Counter.

        Args:
           lines (list): Список строк логов. Каждая строка может быть:
                        - JSON-строкой для парсинга
                        - Уже распарсенным словарем

        Returns:
           dict: Словарь с распределением статус-кодов в формате:
                 {
                     "status_code": count,  # Количество occurrences
                     "200": 1200,
                     "404": 45,
                     "500": 12
                 }

        Notes:
           - Пропускает строки, которые не удается распарсить
           - Конвертирует статус-коды в строки для единообразия
           - Использует Counter для эффективного подсчета
           - Возвращает обычный dict (не Counter) для сериализации
        """

        # Инициализация счетчика для эффективного подсчета
        counter = Counter()

        # Обработка каждой строки лога
        for line in lines:
            obj = _try_parse_json(line)
            if not obj:
                continue

            # Извлечение статус-кода
            code = obj.get("status")

            # Проверка наличия статус-кода
            if code is not None:
                # Конвертация в строку для единообразия и подсчет
                counter[str(code)] += 1

        # Возврат обычного словаря вместо Counter для лучшей сериализации
        return dict(counter)



