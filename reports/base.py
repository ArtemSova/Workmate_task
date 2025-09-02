from abc import ABC, abstractmethod

class BaseReport(ABC):
    """
    Абстрактный базовый класс для всех отчетов анализатора логов.

    Attributes:
        Нет публичных атрибутов

    Methods:
        generate(lines): Абстрактный метод для генерации отчета

    Использование:
    from reports.base import BaseReport

    class CustomReport(BaseReport):
        def generate(self, lines):
            # Реализация генерации отчета
            return processed_data

    Для создания собственного отчета необходимо наследоваться от BaseReport
    и реализовать метод generate().
    """
    @abstractmethod
    def generate(self, lines):
        """
        Генерирует отчет на основе проанализированных строк лога.

        Args:
            lines (list): Список распарсенных строк лога в формате словарей.
                         Каждая строка содержит ключи как минимум:
                         - url: URL endpoint'а
                         - status: HTTP статус-код
                         - response_time: Время ответа в секундах
                         - user_agent: Строка User-Agent
                         - timestamp: Временная метка запроса

        Returns:
            dict: Словарь с обработанными данными отчета. Формат зависит
                 от конкретной реализации отчета.

        Raises:
            NotImplementedError: Если метод не реализован в дочернем классе
            ValueError: Если входные данные некорректны
            KeyError: Если в данных отсутствуют обязательные поля
        """
        pass
