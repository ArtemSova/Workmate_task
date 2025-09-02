from collections import Counter
from utils.log_parser import _try_parse_json
from .base import BaseReport

class UserAgentReport(BaseReport):
    """
    Класс для генерации отчета по распределению User-Agent строк.

    Наследуется от BaseReport и реализует метод generate() для анализа
    частоты встречаемости различных User-Agent строк в логах веб-сервера.

    Attributes:
        Нет публичных атрибутов

    Methods:
        generate(lines): Генерирует отчет со статистикой User-Agent'ов

    Использование:
        from reports.user_agent_report import UserAgentReport

        report = UserAgentReport()
        data = report.generate(parsed_lines)
    """

    def generate(self, lines):
        """
        Анализирует логи и подсчитывает количество каждого User-Agent.

        Обрабатывает каждую строку лога, извлекает User-Agent строку и
        подсчитывает частоту встречаемости каждого уникального User-Agent'а
        с помощью Counter.

        Args:
            lines (list): Список строк логов. Каждая строка может быть:
                         - JSON-строкой для парсинга
                         - Уже распарсенным словарем

        Returns:
            dict: Словарь с распределением User-Agent строк в формате:
                  {
                      "user_agent_string": count,  # Количество occurrences
                      "Mozilla/5.0...": 450,
                      "curl/7.68.0": 89
                  }

        Notes:
            - Пропускает строки, которые не удается распарсить
            - Учитывает только непустые User-Agent строки
            - Сохраняет оригинальные User-Agent строки без модификации
            - Использует Counter для эффективного подсчета
            - Возвращает обычный dict (не Counter) для сериализации
            - Полезен для анализа клиентского ПО, браузеров и ботов
        """

        # Инициализация счетчика для эффективного подсчета
        counter = Counter()

        # Обработка каждой строки лога
        for line in lines:
            # Парсинг JSON или использование готового словаря
            obj = _try_parse_json(line)
            if not obj:
                continue

            # Извлечение User-Agent строки
            ua = obj.get("http_user_agent")

            # Проверка наличия и непустоты User-Agent
            if ua:
                # Подсчет вхождения User-Agent
                counter[ua] += 1

        # Возврат обычного словаря вместо Counter для лучшей сериализации
        return dict(counter)


